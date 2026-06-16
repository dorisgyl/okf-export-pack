---
type: "Reaction"
title: "Websites Angle"
---

## Summary

Slobodan Manic ("Sani"), founder of No Hacks and host of the No Hacks podcast on web strategy for the AI age, argues that Google's Open Knowledge Format — though built for internal company data — solves a problem public websites already have. Today, the most an AI agent gets from a website is a flat, page-by-page markdown copy (via Cloudflare's markdown-for-agents, llms.txt, or direct HTML parsing). That copy drops the relationship layer: it never tells the machine *how* concepts relate to each other, only what each page says individually. A knowledge graph built with OKF keeps that relationship layer intact, so an agent learns not just what each concept is but how they sit relative to one another — "which is most of what understanding a website actually means."

Manic tested the idea on his own site, writing an eight-file OKF bundle covering No Hacks' core concepts (Machine-First Architecture, the agentic web, Agent Experience Optimization, llms.txt, WebMCP, etc.). Each file uses Google's YAML frontmatter conventions and links to sibling concept files with ordinary markdown links — those links *are* the graph. He notes the tradeoff: a bundle is a second copy that must stay in sync with the website, the same maintenance tax every parallel machine-readable layer imposes. He also acknowledges that no AI agent reads website-hosted OKF bundles today — this is a bet on where the format is heading, not a tactic that earns AI citations now.

His speculative trajectory: (1) the thin identity file (llms.txt) could grow into a full knowledge graph; (2) agents could query that map instead of scraping pages, giving site owners more control over how their concepts are represented; (3) the knowledge graph could become the canonical layer, with human-facing pages as just one rendering of it — the "fully machine-first website" the agentic web has been pointing at, "reached through a side door Google opened for internal data."

# Citations

- Blog post: https://nohacks.co/blog/okf-website-knowledge-graph
- LinkedIn post (Slobodan Manic): https://www.linkedin.com/posts/slobodanmanic_google-published-something-yesterday-that-activity-7471496869374836736-Wl-N
