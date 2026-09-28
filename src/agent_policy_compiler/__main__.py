import json,sys
from .core import load,decide
rules=load(sys.argv[1]); acts=json.load(open(sys.argv[2])); print(json.dumps([decide(rules,a) for a in acts],indent=2))
