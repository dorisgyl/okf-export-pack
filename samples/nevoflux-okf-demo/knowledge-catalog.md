---
type: "Product"
title: "Google Cloud Knowledge Catalog (formerly Dataplex)"
resource: "https://cloud.google.com/products/knowledge-catalog"
tags:
  - dataplex
  - google
  - product
---

# Google Cloud Knowledge Catalog

Google Cloud Knowledge Catalog is the rebranded evolution of Dataplex Universal Catalog (itself formerly Data Catalog). Announced at Google Cloud Next on April 22, 2026 by Chai Pydimukkala (Product Lead) and Sam McVeety (Tech Lead, Data Analytics Engineering), the rename clarifies the product's expanded mission without changing its underlying functionality. The product page at cloud.google.com describes it as a "dynamic, always-on, universal context engine for agents" that unifies structured, unstructured, and SaaS data into a governed, agent-ready source of truth.

The Knowledge Catalog operates on three foundational pillars: **Aggregation** (harvesting technical metadata across BigQuery, AlloyDB, Spanner, Cloud SQL, Firestore, Looker, and third-party catalogs like Atlan, Collibra, and DataHub into a single governed source), **Enrichment** (using Gemini to continuously mine schemas, query logs, BI semantic models, and unstructured content to generate business glossaries, entity relationships, and verified SQL patterns), and **Search** (providing high-precision semantic search with sub-second latency, access-control-aware retrieval, and a measurable context evaluation framework). Enterprise connectivity previews include federation with Palantir, Salesforce, SAP, ServiceNow, and Workday.

The Knowledge Catalog is the native ingestion and serving layer for the Open Knowledge Format (OKF). The `GoogleCloudPlatform/knowledge-catalog` GitHub repo hosts reference implementations including enrichment agents, an HTML visualizer, and sample OKF bundles. While tightly integrated with Google Cloud's data stack, the OKF format itself remains platform-independent. Bloomberg Media is cited as an early customer, using Knowledge Catalog to power a Data Access AI Agent grounded in trusted institutional context.

# Citations

- https://cloud.google.com/blog/products/data-analytics/introducing-the-google-cloud-knowledge-catalog
- https://cloud.google.com/products/knowledge-catalog
- https://github.com/GoogleCloudPlatform/knowledge-catalog
