---
type: "Convention"
title: "llms.txt — LLM-Friendly Website Content Convention"
resource: "https://llmstxt.org"
tags:
  - convention
  - llms-txt
---

## Summary

llms.txt is a proposal (by Jeremy Howard / Answer.AI) for websites to provide a `/llms.txt` markdown file at their root path, giving LLMs concise, curated, expert-level information about the site in a single location. The core problem it addresses is that LLM context windows are too small to ingest entire websites, and converting complex HTML with navigation, ads, and JavaScript into clean text is unreliable. The file format is deliberately simple: an H1 title (the only required element), an optional blockquote summary, optional detail paragraphs, and zero or more H2-delimited sections containing link lists with descriptions. The spec also proposes that individual pages offer a clean markdown version at the same URL with `.md` appended. Unlike robots.txt (which governs crawler access) or sitemap.xml (which lists all indexable pages), llms.txt is a curated subset designed for inference-time consumption — when a user or agent explicitly needs context about a site.

llms.txt and Google's Open Knowledge Format (OKF) occupy the same design space: both use markdown as the lingua franca for LLM-readable knowledge, and both rely on lightweight structure (llms.txt uses a positional H1/H2/list convention; OKF uses YAML frontmatter with `type` as the only required field). They are complementary rather than competing: llms.txt is a per-website entry point that tells an LLM *where* to find documentation, while OKF is a portable bundle format that packages *what* the LLM should know into a directory of interlinked markdown files. A site could serve llms.txt as its discovery layer and export its curated knowledge as an OKF bundle. Both descend from the broader "LLM wiki" pattern identified by Karpathy — writing knowledge as markdown for machines to read.

# Citations

- https://llmstxt.org — llms.txt specification and proposal page (browsed)
- https://github.com/AnswerDotAI/llms-txt — GitHub repository hosting the spec
- https://www.fastht.ml/docs/llms.txt — FastHTML project's llms.txt example (referenced on the spec page)
