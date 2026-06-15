# GBrain -> OKF v0.1 mapping

| GBrain (source) | OKF concept (output) | Notes |
|---|---|---|
| page slug `a/b/c` | file `a/b/c.md`, Concept ID `a/b/c` | slug is already path-like; sanitize illegal chars |
| schema-pack `page_type` / frontmatter `type` | `type` (REQUIRED) | fall back to `Concept` if absent; never empty |
| title | `title` | |
| description / first line | `description` | |
| source URL / `resource` / raw_data origin | `resource` | browser-built pages carry the original URL |
| tags | `tags` | |
| updated_at | `timestamp` (ISO 8601) | |
| body | markdown body | use REAL frontmatter, NOT the v1 `\n---\n` split |
| `brain_get_links` (typed) | markdown link, bundle-relative `/a/b/c.md` | LOSSY: link_type dropped; carry the relationship word in prose |
| `brain_get_timeline` / versions | per-page -> optional `## History`; directory-level -> root `log.md` | timeline is per-page, log.md is per-dir |
| takes / facts / salience | optional frontmatter extension keys (e.g. `x-confidence`) | OKF consumers tolerate unknown keys (§4.1) |

## The `---` trap (critical)

The brain crate v1 `BrainPage::from_markdown` splits on `\n---\n` into
compiled_truth/timeline. OKF uses `---` as the **frontmatter delimiter**. They
collide. The serializer always:
- emits the frontmatter block FIRST (line 1 is `---`, then YAML, then `---`), then body;
- treats `brain_get_page` content as plain body — it does not reuse the v1 split;
- a literal `---` inside the body is harmless because frontmatter already closed at top.

## Relationships are prose over untyped links (OKF §5.3)

A link asserts a relationship; the KIND is conveyed by the surrounding sentence,
not by the link. Write e.g. "OKF formalizes the [LLM-wiki pattern](/llm-wiki-pattern.md)".
Prefer bundle-relative absolute links (`/x.md`, §5.1).

## Input JSON schema (what okf-export assembles for build_bundle.py)

```json
{
  "bundle": { "okf_version": "0.1", "bundle_title": "...", "bundle_description": "...",
      "index_intro": "...", "index_sections": [
      { "heading": "...", "items": [ { "title": "...", "target": "/x.md", "desc": "..." } ] } ] },
  "strip":  { "frontmatter_whitelist": ["type","title","description","resource","tags","timestamp"],
              "exclude_prefixes": [".raw/","private/"] },
  "log":    [ { "date": "2026-06-14", "entries": [ { "kind": "Update", "text": "..." } ] } ],
  "pages":  [ { "slug": "a/b", "type": "Spec", "title": "...", "description": "...",
                "resource": "https://...", "tags": ["..."], "timestamp": "2026-06-14T00:00:00Z",
                "body": "prose with /links", "citations": [["title","/references/x.md"]],
                "extra": { "x-confidence": "high" } } ]
}
```

`index_sections` is optional; omit it and the serializer groups by `type`
deterministically.

The export-config fields `bundle_title` / `bundle_description` are passed through
verbatim on the `bundle` object: `bundle_title` becomes the root `index.md`
heading (fallback `Index`), and `bundle_description` becomes the intro paragraph.
If `index_intro` is also set it wins over `bundle_description` (most-specific
override). All three are body content — the root `index.md` frontmatter still
carries only `okf_version` (§11).
