---
type: "Tooling"
title: "OKF Reference Enrichment Agent"
description: "Google's reference producer: a two-pass ADK + Gemini agent that walks BigQuery datasets and produces conformant OKF bundles."
resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/src/enrichment_agent"
tags:
  - adk
  - bigquery
  - gemini
  - google
  - producer
  - tooling
timestamp: "2026-06-15T00:00:00.000Z"
---

# OKF Reference Enrichment Agent

The reference producer shipped alongside the OKF v0.1 spec is an **enrichment agent** that lives in `okf/src/enrichment_agent/` of the `GoogleCloudPlatform/knowledge-catalog` repository. It is built on Google's **Agent Developer Kit (ADK)** and defaults to **Gemini Flash** (`gemini-flash-latest`). Its job is to walk a BigQuery dataset and produce a conformant OKF bundle — one markdown concept file per table or view, with YAML frontmatter, schema documentation, join paths, and cross-links.

The agent uses a deliberate **two-pass architecture** implemented in `runner.py` via the `enrich_all` method. **Pass 1 (BQ enrichment):** For every concept (table/view) discovered by the `Source` abstraction, the `okf_bq_enrichment_agent` is invoked. It has five tools — `list_concepts`, `read_concept_raw`, `sample_rows`, `read_existing_doc`, and `write_concept_doc` — and follows a prompt (`enrichment_instruction.md`) to draft an OKF document with schema, descriptions, sample data, and inter-concept markdown links. **Pass 2 (web ingestion):** After all concepts are drafted, the `okf_web_ingestion_agent` runs a second LLM pass. Given seed URLs and crawl constraints (allowed hosts, path prefixes, max depth, page budget), it fetches authoritative documentation via `fetch_url` and enriches each concept with citations, external references, and verified join paths. A final `regenerate_indexes` step rebuilds all `index.md` files in the bundle directory.

The blog post describes this as: the agent "walks a BigQuery dataset, drafts an OKF concept document for every table and view, then runs a second LLM pass that crawls authoritative documentation and enriches each concept with citations, schemas, and join paths." Three sample bundles (GA4 e-commerce, Stack Overflow, Bitcoin public datasets) are committed to the repo as living examples produced by this agent. The architecture is deliberately a proof of concept — the format is agent-framework-agnostic, and nothing about OKF requires ADK, Gemini, or BigQuery specifically.

# Citations

- OKF enrichment agent source: https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/src/enrichment_agent
- agent.py (two-agent definition): https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/src/enrichment_agent/agent.py
- runner.py (two-pass orchestration): https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/src/enrichment_agent/runner.py
- Google blog post "What we're shipping" section: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
