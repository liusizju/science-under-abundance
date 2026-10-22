SYSTEM_NOTE = """You are participating in a synthetic research-design laboratory. Do not fabricate citations. Return only valid JSON."""

def idea_prompt(corpus_text: str, reward_rule: str, priority_note: str) -> str:
    return f"""{SYSTEM_NOTE}
Using only the conceptual material below, propose one organizational-science research idea.

CORPUS:
{corpus_text}

REWARD RULE:
{reward_rule}

PRIORITY CONTEXT:
{priority_note}

Return JSON with keys: question, mechanism, keywords (3 strings), verification_plan.
"""
