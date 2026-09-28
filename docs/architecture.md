# Architecture

Policies define ordered rule objects with action kind, effect and optional resource pattern. Compilation normalizes and sorts by deny-first specificity. Evaluation is deterministic and defaults closed.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 is a policy compiler/decision engine, not an OS sandbox; enforcement belongs in the caller runtime.
