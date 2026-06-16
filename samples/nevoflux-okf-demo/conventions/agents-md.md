---
type: "Convention"
title: "AGENTS.md / CLAUDE.md — Convention Files for Coding Agents"
resource: "https://agents.md"
tags:
  - agents-md
  - claude-md
  - convention
---

AGENTS.md is an open convention for placing agent-specific instructions in a repository as a plain markdown file. Introduced collaboratively by OpenAI Codex, Amp, Jules (Google), Cursor, and Factory, it complements the human-facing README.md by giving coding agents a predictable file to read before they begin work. The file has no required fields — it is freeform markdown — and covers build steps, test commands, code style, PR guidelines, security considerations, and anything else you would tell a new teammate. In monorepos, nested AGENTS.md files let each subproject ship tailored instructions; the agent reads the closest file in the directory tree. Over 60,000 repositories on GitHub already carry an AGENTS.md. The convention is now stewarded by the Agentic AI Foundation under the Linux Foundation. CLAUDE.md (Anthropic) and .cursorrules (Cursor) serve the same role with vendor-specific naming; AGENTS.md aims to be the vendor-neutral superset that all agents can consume.

Both AGENTS.md and OKF use plain markdown as their medium, but they operate at different layers. AGENTS.md is a per-repository convention file: it lives inside the codebase and tells the agent *how to work on this project* (build commands, style rules, test instructions). OKF is a portable knowledge bundle format: it packages *what the agent should know* (facts, entities, relationships) as a directory of markdown files with YAML frontmatter and a required `type` field. AGENTS.md is imperative ("run these commands, follow these rules"); OKF is declarative ("here are typed knowledge pages"). They are complementary — an OKF bundle could contain a page *about* the AGENTS.md convention, and an AGENTS.md file could instruct the agent to ingest an OKF bundle. Both descend from the broader LLM-wiki pattern: the insight that markdown with lightweight structure is the natural interchange format between humans and language models.

# Citations

- https://agents.md — Official AGENTS.md site (browsed)
- https://openai.com/index/agentic-ai-foundation/ — Agentic AI Foundation announcement
- https://github.com/search?q=path%3AAGENTS.md+NOT+is%3Afork+NOT+is%3Aarchived&type=code — 60k+ AGENTS.md files on GitHub
