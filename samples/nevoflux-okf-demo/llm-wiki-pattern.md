---
type: "Pattern"
title: "The LLM-Wiki Pattern"
description: "A pattern for building personal knowledge bases using LLMs — write knowledge as frontmatter-bearing markdown, let LLMs maintain a living wiki. OKF is its formalization."
resource: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
tags:
  - karpathy
  - llm-wiki
  - pattern
timestamp: "2026-06-15T00:00:00.000Z"
---

# The LLM-Wiki Pattern

The LLM-wiki pattern, articulated most crisply by Andrej Karpathy in his viral GitHub gist "LLM Wiki" (5,000+ stars), replaces the traditional RAG loop with a persistent, compounding knowledge base. Instead of retrieving raw document chunks on every query, the LLM incrementally builds and maintains a structured wiki — a directory of interlinked markdown files with YAML frontmatter. When a new source is ingested, the LLM reads it, extracts key information, writes summary pages, updates entity and concept pages, maintains cross-references, and flags contradictions. The wiki is the compiled artifact; the LLM is the compiler. Karpathy's three-layer architecture consists of immutable **raw sources** (articles, papers, data), the **wiki** itself (LLM-generated and LLM-maintained markdown), and a **schema file** (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM the wiki's conventions and workflows. "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass," Karpathy writes — the bookkeeping that causes humans to abandon personal wikis is exactly what LLMs excel at.

The pattern has a rich lineage. As the Google Cloud blog post introducing OKF notes, the knowledge-as-wiki pattern "keeps reappearing under different names": **Obsidian vaults** wired to coding agents, the **AGENTS.md / CLAUDE.md** family of convention files that tell agents how a project is structured, repos full of index.md and log.md artifacts that agents consult before doing real work, and **"metadata as code" repositories** inside data teams. Each instance looks alike — markdown, frontmatter, cross-links — but none are intentionally designed to cooperate. There is no agreed-upon answer to what fields every document should carry or what filenames mean.

The **Open Knowledge Format (OKF)**, introduced by Sam McVeety and Amir Hormati at Google Cloud, is the formalization of this pattern into a portable, interoperable standard. OKF v0.1 formalizes the small set of conventions needed to make these bespoke wikis interoperable: a directory of markdown files with YAML frontmatter, where `type` is the only required field. No SDK, no runtime, no proprietary platform. As the blog post states: "the value of a knowledge format comes from how many parties speak it, not from who owns it." OKF turns the LLM-wiki pattern from a collection of ad-hoc implementations into a lingua franca.

# Citations

- Karpathy, Andrej. "LLM Wiki." GitHub Gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- McVeety, Sam and Hormati, Amir. "Introducing the Open Knowledge Format." Google Cloud Blog, June 12, 2026. https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- OKF Spec (v0.1). https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
