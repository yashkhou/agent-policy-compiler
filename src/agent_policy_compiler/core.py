from dataclasses import dataclass
from fnmatch import fnmatch
import tomllib
@dataclass(frozen=True)
class Rule: effect:str; kind:str; pattern:str='*'; reason:str=''
def load(path):
 d=tomllib.load(open(path,'rb')); return compile_rules(d.get('rule',[]))
def compile_rules(rows):
 rules=[Rule(x['effect'],x['kind'],x.get('pattern','*'),x.get('reason','')) for x in rows]
 if any(r.effect not in ('allow','deny') for r in rules): raise ValueError('effect must be allow or deny')
 return sorted(rules,key=lambda r:(0 if r.effect=='deny' else 1,-len(r.pattern),r.kind,r.pattern))
def decide(rules,action):
 target=action.get('target',''); kind=action['kind']
 for r in rules:
  if r.kind in ('*',kind) and fnmatch(target,r.pattern): return {'allowed':r.effect=='allow','rule':r.__dict__,'action':action}
 return {'allowed':False,'rule':None,'action':action,'reason':'default deny'}
