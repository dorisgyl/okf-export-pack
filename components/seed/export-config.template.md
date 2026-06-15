---
type: OKF Export Config
title: OKF Export Config
---

Edit this page to control what `okf-export` includes and how it strips. The skill
reads these fenced values.

# Scope (a page is included if it matches any prefix or tag)
```
include_prefixes: ["okf-demo/"]
include_tags: []
```

# Privacy (enforced deterministically by the serializer, not by prompt)
```
frontmatter_whitelist: ["type", "title", "description", "resource", "tags", "timestamp"]
exclude_prefixes: [".raw/", "private/"]
```

# Bundle metadata
```
bundle_title: "NevoFlux x OKF - a browser-built knowledge bundle"
bundle_description: "An OKF bundle exported from NevoFlux GBrain memory."
okf_version: "0.1"
```
