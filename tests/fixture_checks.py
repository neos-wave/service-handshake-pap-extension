"""Check consistency of illustrative exchanges, never live authority or execution.

These helpers deliberately inspect supplied fixtures. They do not authenticate a
sender, retrieve evidence, interpret free-form user instructions, or implement a
service gateway. The header parser covers the canonical header subset used in
these examples; production implementations need a complete Structured Fields
parser.
"""

from datetime import datetime
import re

EXT = "dualcx.com/service-handshake"
VERSION = "3"
DRAFT = "2026-11-25"


def parse_extensions_header(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing Poppy-Extensions request selection")
    selected = {}
    for part in value.split(","):
        match = re.fullmatch(r'\s*"([^"\\]+)"\s*;\s*v="([0-9]+)"\s*', part)
        if not match:
            raise ValueError("malformed fixture Poppy-Extensions selection")
        name, version = match.groups()
        if name in selected:
            raise ValueError("duplicate extension request selection")
        selected[name] = version
    return selected


def check_fixture_negotiation(value, company, context):
    """Check advertised support against an actual request header and local config."""
    headers = context.get("headers", {})
    if company.get("protocol_version") != "1.0" or headers.get("Poppy-Version") != "1.0":
        raise ValueError("fixture must select the pinned Poppy 1.0 document")
    selected = parse_extensions_header(headers.get("Poppy-Extensions"))
    support = context.get("local_support", {})
    advertised = company.get("extensions", {})
    configurations = {}
    for name, version in selected.items():
        entries = advertised.get(name, [])
        if not isinstance(entries, list):
            raise ValueError("Company extensions must be arrays of version entries")
        matches = [entry for entry in entries if entry.get("version") == version]
        if len(matches) != 1 or support.get(name, {}).get("version") != version:
            raise ValueError("selected extension version is not supported by both implementations")
        configurations[name] = matches[0]
    if EXT in selected:
        company_config = configurations[EXT]
        local_config = support[EXT]
        if selected[EXT] != VERSION or any(
            config.get("draft_revision") != DRAFT
            for config in (company_config, local_config)
        ):
            raise ValueError("inspect the exact Company draft before selecting extension 3")
        if not set(company_config.get("required_actions", [])) <= set(company_config.get("actions", [])):
            raise ValueError("required actions exceed the Company's declared scope")
    message_extensions = value.get("message", {}).get("extensions", {})
    for name in message_extensions:
        if name not in selected:
            raise ValueError("extension payload was sent without request selection")
    if EXT in message_extensions:
        record = message_extensions[EXT]
        if record.get("version") != VERSION or record.get("draft_revision") != DRAFT:
            raise ValueError("payload disagrees with selected extension version or draft")
        action = record.get("proposal", {}).get("action_type")
        if action and any(action not in config.get("actions", []) for config in (configurations[EXT], support[EXT])):
            raise ValueError("proposal falls outside declared extension action coverage")
    if "operations" in message_extensions:
        if selected.get("operations") != "3" or EXT not in selected:
            raise ValueError("this fixture binding requires Operations 3 and Service Handshake selection")
        if not all(config.get("operations_binding") for config in (configurations[EXT], support[EXT])):
            raise ValueError("SH Operations binding is not supported by both implementations")


def check_message_semantics(value):
    """Fixture placement and claimed sender checks, not sender authentication."""
    message = value["message"]
    company = value.get("type") == "message" and message.get("role") == "company"
    extensions = message.get("extensions", {})
    operations = extensions.get("operations", {})
    if any(key in message for key in ("sender", "operation", "approval", "declined")):
        raise ValueError("legacy message field")
    if EXT in message.get("data", {}):
        raise ValueError("legacy SH placement")
    if value.get("type") != "message" and any(key in message for key in ("role", "id")):
        raise ValueError("client request uses a top-level id, not message.id or role")
    if not company and any(key in message["author"] for key in ("id", "name", "image")):
        raise ValueError("client company-author fields")
    if any(key in operations for key in ("operation", "declined")) and not company:
        raise ValueError("client cannot issue an operation or decline")
    if "approval" in operations and (company or message["author"]["type"] != "agent"):
        raise ValueError("approval sender")
    if company and "context" in message:
        raise ValueError("company context")
    if not company and any(key in extensions for key in ("links", "disclosures")):
        raise ValueError("company-only extension")
    record = extensions.get(EXT)
    if record:
        if record["type"] in ("assessment", "operation_binding") and not company:
            raise ValueError("client trusted company record")
        if record["type"] == "operation_binding":
            operation = operations.get("operation")
            if not operation or any(operation[key] != record[key] for key in ("operation_id", "revision")):
                raise ValueError("operation binding mismatch")
        if record["type"] == "assessment" and record["decision"] == "allow":
            if datetime.fromisoformat(record["valid_until"]) <= datetime.fromisoformat(record["assessed_at"]):
                raise ValueError("allow interval")
    if "operation" in operations:
        if not record or record["type"] != "operation_binding":
            raise ValueError("unbound SH example operation")
        if any(key in operations["operation"] for key in ("state", "confirmation", "result", "user_approval_required", EXT)):
            raise ValueError("legacy operation")
    if "declined" in operations:
        if not record or record["type"] != "assessment" or record["decision"] == "allow":
            raise ValueError("native decline must accompany a non-allow SH assessment")
        operation_ref = record["proposal"].get("operation", {})
        if any(operation_ref.get(key) != operations["declined"][key] for key in ("operation_id", "revision")):
            raise ValueError("decline assessment binding mismatch")


def check_agent_instruction(operation, approval, instruction):
    """Compare this appointment fixture's structured bounds, without NLP or proof."""
    if not instruction or instruction.get("source") != "personal_agent_user_interface":
        raise ValueError("agent approval needs an explicit prior User instruction fixture")
    if not instruction.get("text") or not instruction.get("received_at"):
        raise ValueError("prior User instruction needs its text and time")
    if "reference" in approval and instruction.get("record_ref") != approval["reference"]:
        raise ValueError("approval does not refer to its supplied User instruction record")
    if "approved_at" in approval and datetime.fromisoformat(instruction["received_at"]).timestamp() > approval["approved_at"]:
        raise ValueError("instruction must precede the agent approval")
    terms = operation["terms"]
    constraints = instruction.get("constraints")
    if not isinstance(constraints, dict) or not constraints:
        raise ValueError("no structured instruction bounds for this offline comparison")
    covered = (set(constraints) - {"earliest_start", "latest_end", "max_fee"}) | {"start", "end", "fee"}
    if not set(terms) <= covered:
        raise ValueError("operation adds terms not covered by the supplied User instruction")
    start = datetime.fromisoformat(terms["start"])
    end = datetime.fromisoformat(terms["end"])
    if start.tzinfo is None or end.tzinfo is None or end <= start:
        raise ValueError("appointment interval must have offsets and a later end")
    if (end - start).total_seconds() != terms["duration_minutes"] * 60:
        raise ValueError("appointment interval does not match its approved duration")
    for key, expected in constraints.items():
        if key == "earliest_start":
            if datetime.fromisoformat(terms["start"]) < datetime.fromisoformat(expected):
                raise ValueError("appointment starts before the User's allowed window")
        elif key == "latest_end":
            if datetime.fromisoformat(terms["end"]) > datetime.fromisoformat(expected):
                raise ValueError("appointment ends after the User's allowed window")
        elif key == "max_fee":
            fee = terms["fee"]
            if not isinstance(fee, dict) or set(fee) != set(expected):
                raise ValueError("nested fee terms are not exactly covered by the User's instruction")
            if any(fee[name] != limit for name, limit in expected.items() if name != "amount_minor") or fee["amount_minor"] > expected["amount_minor"]:
                raise ValueError("appointment fee exceeds the User's instruction")
        elif terms.get(key) != expected:
            raise ValueError("operation terms do not satisfy the User's instruction: " + key)


def check_operation_bindings(values):
    """Check case/proposal ownership of each supplied operation-revision tuple."""
    bindings = {}
    for value in values:
        extensions = value["message"].get("extensions", {})
        operation = extensions.get("operations", {}).get("operation")
        if operation is None:
            continue
        record = extensions.get(EXT, {})
        if record.get("type") != "operation_binding":
            raise ValueError("operation has no Service Handshake binding")
        key = (operation["operation_id"], operation["revision"])
        binding = (record["case_ref"], record["proposal_ref"])
        if key in bindings and bindings[key] != binding:
            raise ValueError("operation revision was rebound to a different case or proposal")
        bindings[key] = binding
    for value in values:
        extensions = value["message"].get("extensions", {})
        content = extensions.get("operations", {})
        record = extensions.get(EXT, {})
        references = [content[name] for name in ("approval", "declined") if name in content]
        operation_ref = record.get("proposal", {}).get("operation")
        if operation_ref:
            references.append(operation_ref)
        for reference in references:
            key = (reference["operation_id"], reference["revision"])
            if key not in bindings:
                raise ValueError("record references an unbound operation revision")
        if operation_ref:
            key = (operation_ref["operation_id"], operation_ref["revision"])
            if (record["case_ref"], record["proposal"]["proposal_ref"]) != bindings[key]:
                raise ValueError("assessment case or proposal does not match its operation binding")


def check_fixture_lifecycle(values, instructions=None):
    """Check observable offer/approval/decline ordering in a supplied fixture trace.

    This detects invalid example traces; it does not prove runtime enforcement,
    actual approval, freshness of evidence, or that any operation executed.
    """
    instructions = instructions or {}
    check_operation_bindings(values)
    operations = {}
    offered_at = {}
    approvals = set()
    declined = set()
    recovery_needs_user = set()
    last_approval = {}
    revision_needs_user = set()
    for value in values:
        check_message_semantics(value)
        content = value["message"].get("extensions", {}).get("operations", {})
        if "operation" in content:
            operation = content["operation"]
            key = (operation["operation_id"], operation["revision"])
            if key in operations and any(operations[key][field] != operation[field] for field in ("terms", "expires_at")):
                raise ValueError("immutable operation revision changed")
            previous = last_approval.get(key[0])
            if previous and previous["revision"] != key[1] and previous["approver"] == "agent":
                revision_needs_user.add(key)
            operations[key] = operation
            if key not in offered_at and "created_at" in value:
                offered_at[key] = datetime.fromisoformat(value["created_at"]).timestamp()
        if "approval" in content:
            approval = content["approval"]
            key = (approval["operation_id"], approval["revision"])
            if key not in operations:
                raise ValueError("approval references an unseen operation revision")
            if key in declined:
                raise ValueError("a declined approval must never be sent again")
            fresh_user_required = key[0] in recovery_needs_user or key in revision_needs_user
            if fresh_user_required and approval["approver"] != "user":
                raise ValueError("recovery or revised agent-approved terms require fresh User approval")
            # Optional metadata can expose an inconsistent fixture, but its
            # absence is not a native validation failure or evidence of consent.
            if "approved_at" in approval and key in offered_at and approval["approved_at"] < offered_at[key]:
                raise ValueError("approval metadata predates the fixture's offered revision")
            previous = last_approval.get(key[0], {})
            if fresh_user_required:
                if "reference" in approval and approval["reference"] == previous.get("reference"):
                    raise ValueError("fresh User approval reused the previous approval record reference")
                if "approved_at" in approval and "approved_at" in previous and approval["approved_at"] < previous["approved_at"]:
                    raise ValueError("fresh User approval metadata predates the previous approval")
            if approval["approver"] == "agent":
                check_agent_instruction(operations[key], approval, instructions.get(value.get("id")))
            approvals.add(key)
            last_approval[key[0]] = approval
            if approval["approver"] == "user":
                recovery_needs_user.discard(key[0])
                revision_needs_user.discard(key)
        if "declined" in content:
            decline = content["declined"]
            key = (decline["operation_id"], decline["revision"])
            if key not in approvals:
                raise ValueError("a pre-approval hold is not a native approval decline")
            declined.add(key)
            recovery_needs_user.add(key[0])


def check_handover_continuity(assessment_records, handover):
    """Preserve still-present reasons, including an earlier hold during escalation."""
    outstanding = {}
    for assessment in assessment_records:
        if assessment["case_ref"] != handover["case_ref"]:
            raise ValueError("handover cannot carry another case's restrictions")
        proposal = assessment["proposal"]["proposal_ref"]
        previous = outstanding.get(proposal, {})
        if assessment["decision"] == "allow":
            outstanding[proposal] = {}
        else:
            outstanding[proposal] = {
                reason["code"]: previous.get(reason["code"], assessment["decision"])
                for reason in assessment["reasons"]
            }
    required = {(proposal, decision) for proposal, reasons in outstanding.items() for decision in reasons.values()}
    actual = {(restriction["proposal_ref"], restriction["decision"]) for restriction in handover["restrictions"]}
    if not required <= actual:
        raise ValueError("handover dropped an unresolved hold, denial or escalation")
    if not {proposal for proposal, _ in required} <= set(handover["proposal_refs"]):
        raise ValueError("handover omitted a restricted proposal")
