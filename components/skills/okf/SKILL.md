---
name: okf
description: Host skill carrying OKF export conventions (mapping, conformance, privacy) and the serializer script. Not invoked directly; read by okf-export via skill_read.
allowed-tools: []
---

# OKF (host skill)

This skill ships shared contracts and the deterministic serializer for OKF export.
It is not run on its own. The `okf-export` worker reads from it:

- `conventions/mapping.md` — GBrain -> OKF v0.1 field mapping (and the `---` trap)
- `conventions/conformance.md` — OKF v0.1 conformance rules this pack enforces
- `conventions/privacy.md` — strip / whitelist rules
- `scripts/build_bundle.py` — the serializer (stdlib-only); staged to $SESSION_DIR and run via the `okf.build` canvas-tool
