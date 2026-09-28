# agent-policy-compiler

Compile human-readable capability policies into deterministic guards for filesystem, network and process actions.

## What it does

- reads standard TOML with Python tomllib
- compiles allow/deny rules into canonical priority order
- matches path globs, host globs and process names
- returns explainable allow/deny decisions including the rule that won

## Quick start

```bash
PYTHONPATH=src python -m agent_policy_compiler examples/policy.toml examples/actions.json
```

No model API, network service, or third-party package is required.

## Architecture

Policies define ordered rule objects with action kind, effect and optional resource pattern. Compilation normalizes and sorts by deny-first specificity. Evaluation is deterministic and defaults closed.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 is a policy compiler/decision engine, not an OS sandbox; enforcement belongs in the caller runtime.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.
