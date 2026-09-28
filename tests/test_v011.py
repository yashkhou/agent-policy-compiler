import unittest

from agent_policy_compiler.core import batch_decide, compile_rules, explain, lint


class PolicyUpgradeTests(unittest.TestCase):
    def test_explicit_higher_priority_allow_can_override_broad_deny(self):
        rules = compile_rules([
            {"effect": "deny", "kind": "network", "pattern": "*", "priority": 0},
            {"effect": "allow", "kind": "network", "pattern": "api.example.com", "priority": 10},
        ])
        result = explain(rules, {"kind": "network", "target": "api.example.com"})
        self.assertTrue(result["allowed"])
        self.assertEqual(result["rule"]["priority"], 10)
        self.assertTrue(result["trace"][0]["matched"])

    def test_linter_flags_shadowed_rule(self):
        rules = compile_rules([
            {"effect": "deny", "kind": "filesystem", "pattern": "*", "priority": 5},
            {"effect": "allow", "kind": "filesystem", "pattern": "/tmp/*", "priority": 0},
        ])
        self.assertIn("shadowed-by-catch-all", {finding["code"] for finding in lint(rules)})

    def test_batch_decision_is_fail_closed(self):
        rules = compile_rules([])
        self.assertEqual([x["allowed"] for x in batch_decide(rules, [{"kind": "x"}, {"kind": "y"}])], [False, False])


if __name__ == "__main__":
    unittest.main()
