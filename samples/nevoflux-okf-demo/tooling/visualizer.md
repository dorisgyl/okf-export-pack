---
type: "Tooling"
title: "OKF Static Visualizer"
description: "A single-file HTML viewer that renders any OKF bundle as an interactive force-directed graph — no backend, no install, no data leaves the page."
resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf"
tags:
  - consumer
  - google
  - tooling
---

The OKF visualizer (`okf/src/enrichment_agent/viewer/`) is a proof-of-concept *consumer* of the Open Knowledge Format, mirroring the enrichment agent as a proof-of-concept *producer*. Running `python -m enrichment_agent visualize --bundle ./bundles/<name>` walks every `.md` file in a bundle, parses its YAML frontmatter and markdown body, extracts cross-links via regex, and writes a single self-contained `viz.html` file. The generator (`viewer/generator.py`, 175 lines) builds a Cytoscape.js graph data structure — nodes from concepts (colored by type via a palette: purple for BigQuery Dataset, blue for BigQuery Table, green for Reference), edges from markdown cross-links — and serializes the entire bundle as a JSON blob embedded in an HTML template. The template loads Cytoscape.js and marked.js from CDN for graph rendering and in-browser markdown rendering respectively. No data leaves the page; the bundle is parsed once at generation time.

The viewer ships features that make it genuinely useful for exploring OKF bundles: a **force-directed graph** (with switchable layouts: cose, concentric, breadth-first, circle, grid), a **detail panel** showing frontmatter metadata and the rendered markdown body for any selected concept, computed **"Cited by" backlinks** (reverse link graph), a **search box** (matching title, concept ID, and tags), and a **type filter**. Internal `[...](/path/to/concept.md)` links in the markdown body are rewired to navigate within the viewer rather than following file paths. Node size scales with document length (`30 + min(60, len(body) // 200)` pixels). Three ready-to-browse viz.html files ship checked into the repo alongside the sample bundles: GA4 e-commerce, Stack Overflow, and Bitcoin blocks/transactions.

# Citations

- OKF README (Visualize section): https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
- viewer/generator.py source: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/src/enrichment_agent/viewer/generator.py
- Viewer directory (static/, templates/): https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/src/enrichment_agent/viewer
