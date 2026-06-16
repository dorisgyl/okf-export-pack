---
type: "Tooling"
title: "NevoFlux OKF Export Pack"
resource: "https://github.com/dorisgyl/okf-export-pack"
tags:
  - independent
  - nevoflux
  - producer
  - tooling
---

The NevoFlux OKF Export Pack is a skill-based plugin for the NevoFlux browser agent that projects a user's GBrain — the browser's persistent, agent-managed knowledge base — into a conformant OKF v0.1 bundle directory. It maps GBrain's native page model (slug hierarchy, YAML frontmatter with `type`/`tags`/`resource`/`timestamp`, markdown body, inter-page links) onto OKF's directory-of-markdown convention, handling conformance requirements (non-empty `type` field, parseable frontmatter), privacy filtering, and citation preservation. The pack consists of a host skill (`okf`) carrying the mapping rules, conformance checks, and serializer script, plus an export skill (`okf-export`) that orchestrates page selection, transformation, and bundle output.

As an independent, non-Google OKF producer, the NevoFlux OKF Export Pack is among the earliest third-party implementations of the Open Knowledge Format specification. While Google's reference producer walks BigQuery datasets using ADK + Gemini, this pack operates on a fundamentally different source: a personal knowledge base built through browser-assisted research, web capture, and manual curation. It demonstrates that OKF's vendor-neutral design works as advertised — no dependency on Google Cloud, BigQuery, ADK, or Gemini. The bundle you are reading was itself produced by this pack.

# Citations

- OKF Export Pack repository: https://github.com/dorisgyl/okf-export-pack
- OKF v0.1 Specification: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
