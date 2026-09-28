import unittest,sys; sys.path.insert(0,'src')
from agent_policy_compiler.core import *
class T(unittest.TestCase):
 def test_allow(self): self.assertTrue(decide(compile_rules([{'effect':'allow','kind':'network','pattern':'api.*'}]),{'kind':'network','target':'api.github.com'})['allowed'])
 def test_default_deny(self): self.assertFalse(decide([] ,{'kind':'process','target':'bash'})['allowed'])
 def test_deny_precedes_allow(self):
  r=compile_rules([{'effect':'allow','kind':'filesystem','pattern':'**'},{'effect':'deny','kind':'filesystem','pattern':'**/.ssh/**'}]); self.assertFalse(decide(r,{'kind':'filesystem','target':'home/.ssh/key'})['allowed'])
