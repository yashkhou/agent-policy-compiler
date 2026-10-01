> [!IMPORTANT]
> **This project now lives in [agent-reliability-lab](https://github.com/yashkhou/agent-reliability-lab/tree/main/packages/agent-policy-compiler).** Its full history was moved there and this repository is archived.
>
> `pip install "git+https://github.com/yashkhou/agent-reliability-lab#subdirectory=packages/agent-policy-compiler"`


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


## v0.1.1

**Priority-aware policy explanations and linting.** Rules now support explicit priorities, decision traces, batch evaluation, and lint findings for duplicates or catch-all shadowing while default-deny remains intact.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
