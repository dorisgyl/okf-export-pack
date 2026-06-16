---
type: "Spec"
title: "Open Knowledge Format (OKF) v0.1"
description: "An open, vendor-neutral specification for representing knowledge as markdown files with YAML frontmatter, designed for both humans and AI agents."
resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
tags:
  - google
  - okf
  - spec
timestamp: "2026-06-12T00:00:00.000Z"
---

# Open Knowledge Format (OKF) v0.1

The Open Knowledge Format (OKF) is an open, vendor-neutral specification for representing *knowledge* — the metadata, context, and curated insight that surrounds data and systems. Published as a v0.1 draft by Google Cloud engineers Sam McVeety (Tech Lead, Data Analytics) and Amir Hormati (Tech Lead, BigQuery), OKF formalizes the emerging "LLM wiki" pattern into a portable, interoperable standard. A knowledge bundle is simply a directory of UTF-8 markdown files with YAML frontmatter — no schema registry, no central authority, no required SDK or runtime. If you can `cat` a file or `git clone` a repo, you can read and ship OKF.

The spec is intentionally minimal: the only required field in every concept document's frontmatter is `type`, a short string identifying the kind of concept (e.g. "BigQuery Table", "Playbook", "Metric"). Type values are not centrally registered; producers pick descriptive values and consumers must tolerate unknown types gracefully. All other frontmatter fields — `title`, `description`, `resource`, `tags`, `timestamp` — are recommended but optional. Concepts link to each other via standard markdown links, forming a navigable graph. Bundles may include `index.md` files for progressive disclosure and `log.md` files for change history. Conformance is straightforward: every non-reserved `.md` file must have parseable YAML frontmatter with a non-empty `type` field.

OKF ships as part of Google Cloud's Knowledge Catalog repository on GitHub, alongside reference implementations: an enrichment agent that generates OKF bundles from BigQuery datasets, a static HTML graph visualizer, and three sample bundles (GA4 e-commerce, Stack Overflow, Bitcoin public datasets). However, OKF itself is format-only — it is not tied to any cloud, database, model provider, or agent framework, and will never require a proprietary account or SDK. Google Cloud's Knowledge Catalog has been updated to ingest OKF and serve it to agents, but the spec is designed for broad adoption beyond Google products.

OKF formalizes the [LLM-Wiki Pattern](/llm-wiki-pattern.md) into a portable standard. It ships inside [Google Cloud Knowledge Catalog](/knowledge-catalog.md). Related conventions include [llms.txt](/conventions/llms-txt.md) and [AGENTS.md](/conventions/agents-md.md).

# Citations

[1] [OKF SPEC.md — GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
[2] [Introducing the Open Knowledge Format — Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
[3] [GoogleCloudPlatform/knowledge-catalog — GitHub](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
