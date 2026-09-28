from __future__ import annotations

from dataclasses import asdict, dataclass
from fnmatch import fnmatch
import tomllib


@dataclass(frozen=True)
class Rule:
    effect: str
    kind: str
    pattern: str = "*"
    reason: str = ""
    priority: int = 0


def load(path):
    with open(path, "rb") as handle:
        data = tomllib.load(handle)
    return compile_rules(data.get("rule", []))


def compile_rules(rows):
    rules = [Rule(x["effect"], x["kind"], x.get("pattern", "*"), x.get("reason", ""), int(x.get("priority", 0))) for x in rows]
    if any(rule.effect not in ("allow", "deny") for rule in rules):
        raise ValueError("effect must be allow or deny")
    return sorted(rules, key=lambda rule: (-rule.priority, 0 if rule.effect == "deny" else 1, -len(rule.pattern), rule.kind, rule.pattern))


def _matches(rule: Rule, action: dict) -> bool:
    return rule.kind in ("*", action["kind"]) and fnmatch(action.get("target", ""), rule.pattern)


def explain(rules, action):
    trace = []
    selected = None
    for index, rule in enumerate(rules):
        matched = _matches(rule, action)
        trace.append({"index": index, "matched": matched, "rule": asdict(rule)})
        if matched:
            selected = rule
            break
    if selected is None:
        return {"allowed": False, "rule": None, "action": action, "reason": "default deny", "trace": trace}
    return {
        "allowed": selected.effect == "allow",
        "rule": asdict(selected),
        "action": action,
        "reason": selected.reason or f"matched {selected.effect} rule",
        "trace": trace,
    }


def decide(rules, action):
    result = explain(rules, action)
    result.pop("trace")
    return result


def batch_decide(rules, actions):
    return [decide(rules, action) for action in actions]


def lint(rules):
    findings = []
    seen = set()
    for index, rule in enumerate(rules):
        signature = (rule.effect, rule.kind, rule.pattern, rule.priority)
        if signature in seen:
            findings.append({"index": index, "code": "duplicate-rule", "rule": asdict(rule)})
        seen.add(signature)
        for earlier in rules[:index]:
            if earlier.pattern == "*" and earlier.kind in ("*", rule.kind) and earlier.priority >= rule.priority:
                findings.append({"index": index, "code": "shadowed-by-catch-all", "rule": asdict(rule), "by": asdict(earlier)})
                break
    return findings
