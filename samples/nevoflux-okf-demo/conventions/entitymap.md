---
type: "Convention"
title: "Entitymap"
resource: "https://entitymap.org/spec/v0.4"
tags:
  - community
  - convention
  - entitymap
---

# EntityMap

EntityMap is a community-driven open standard (v0.4, CC BY 4.0) for publishing a structured, entity-first index of website knowledge for AI agents, RAG pipelines, and LLM-based applications. Created by Fred Laurent and Dixon Jones (CEO of InLinks / Waikay), it entered public consultation in June 2026 with formal launch scheduled for July 1, 2026. R.V. Guha, one of the founders of schema.org, has endorsed the project. Unlike OKF's markdown-with-YAML-frontmatter approach, EntityMap uses a JSON file (`entitymap.json`) served at the domain root, alongside an HTML companion (`entitymap.html`) that embeds per-entity JSON-LD for schema.org interoperability. Where sitemap.xml tells crawlers *what pages exist*, EntityMap tells AI systems *what an organization knows and how that knowledge connects*.

The spec is built around three core elements: **Entities** (named things — products, people, concepts, each typed via schema.org `@type`), **Relations** (typed directional links between entities using a controlled predicate vocabulary of 43 standard predicates — 18 core, 25 extended), and **Evidence Chunks** (1-5 extractive passages per entity, each carrying publisher attribution, source URL, retrieval timestamp, and optional relevance score). Required fields span ~12 across three objects (root, entity, chunk). Publisher attribution is a first-class concern: the `publisher` field appears at root level and on every chunk to survive extraction into vector databases, and the HTML companion requires visible plain-text attribution in `<cite>` elements to survive plain-text LLM pipelines. Sites with 200+ entities can shard into typed files (concepts, people, products, places).

As a positioning contrast with Google's OKF: EntityMap is **publisher-facing and web-native** — designed for organizations to declare their knowledge to external AI consumers, with strong emphasis on brand attribution and anti-hallucination. OKF is **agent-facing and portable** — designed as a bundle format for AI agents to carry and share knowledge internally, with `type` as the only required field and no attribution machinery. EntityMap uses JSON with schema.org types and a formal predicate vocabulary; OKF uses markdown with YAML frontmatter and freeform content. They address different layers: EntityMap is a discovery/assertion layer ("here's what we know"), OKF is a knowledge-transfer layer ("here's what the agent should remember"). Both descend from the broader trend of making knowledge LLM-readable, but they are complementary rather than competing.

# Citations

- EntityMap Specification v0.4: https://entitymap.org/spec/v0.4
- Search Engine Journal article by Dixon Jones (June 1, 2026): https://www.searchenginejournal.com/entitymap-the-open-standard-that-gives-ai-systems-a-structured-view-of-your-business/576146/
- GitHub repository: https://github.com/entitymap/entitymap
