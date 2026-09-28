# Implementation note

Working V1 scope: Compile human-readable capability policies into deterministic guards for filesystem, network and process actions.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 is a policy compiler/decision engine, not an OS sandbox; enforcement belongs in the caller runtime.
