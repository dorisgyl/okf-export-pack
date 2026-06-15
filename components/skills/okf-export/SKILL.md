---
name: okf-export
description: Export selected GBrain pages as a conformant Open Knowledge Format (OKF) v0.1 bundle directory.
allowed-tools:
  - brain_get_page
  - brain_search
  - brain_list
  - brain_get_links
  - brain_get_timeline
  - brain_put_page
  - read_file
  - write_file
  - skill_read
  - okf.build
  - okf.pack
---

# OKF Export

Project a selection of GBrain pages into a conformant OKF v0.1 bundle. The
mapping/conformance/privacy rules live in the `okf` host skill; read them first.
Serialization is deterministic (a Python script), not free-handed by you — your
job is selection, fetching, assembling the input JSON, and surfacing the report.

> Tool-name note: `brain_get_links`, `brain_get_timeline`, and `brain_list` are
> assumed to follow the `brain_<gbrain-name>` convention. If any call returns
> "unknown tool", look it up in the live registry — a mismatched `allowed-tools`
> entry is silently dropped, with no error.

## Step 0 — read the contracts (always first)

- `skill_read('okf', 'conventions/mapping.md')`
- `skill_read('okf', 'conventions/conformance.md')`
- `skill_read('okf', 'conventions/privacy.md')`

## Step 1 — stage the serializer

Read the canonical serializer and write it verbatim into the session dir so the
canvas-tool can run it. Do not re-derive or edit it:

1. `skill_read('okf', 'scripts/build_bundle.py')`
2. `write_file('$SESSION_DIR/build_bundle.py', <verbatim contents>)`

## Step 2 — read the export config

`brain_get_page('okf/export-config')`. Parse the fenced values: `include_prefixes`,
`include_tags`, `frontmatter_whitelist`, `exclude_prefixes`, `bundle_title`,
`bundle_description`, `okf_version`. If the page is missing, stop and tell the
user to install/seed it.

## Step 3 — select pages

Resolve the slug set from the config:
- for each prefix in `include_prefixes`: `brain_list` (or `brain_search`) and keep
  slugs under that prefix;
- for each tag in `include_tags`: `brain_search` and keep tagged slugs.
Union them; drop any slug under an `exclude_prefixes` entry (belt-and-suspenders —
the serializer strips these too).

## Step 4 — fetch each page and assemble input

For every selected slug:
- `brain_get_page(slug)` → frontmatter + body. Treat the returned content as the
  OKF **body**; build OKF frontmatter from the page's metadata per `mapping.md`.
  Do NOT reuse any `compiled_truth\n---\ntimeline` split — see the `---` trap.
- `brain_get_links(slug)` → for each outgoing link, render a bundle-relative
  markdown link `/<target>.md` inside a prose sentence that names the relationship
  (OKF links are untyped; the relationship word is prose-only).
- `brain_get_timeline(slug)` → fold into the bundle-level `log` entries (per-page
  timeline becomes directory-level log, per `mapping.md`).

Build a single JSON object (see `mapping.md` for the exact schema) with
`bundle`, `strip` (from the config whitelist/exclude), `log`, and `pages[]`.
Put the config's `bundle_title` / `bundle_description` straight onto `bundle`
(same key names) — the serializer consumes them for the index heading and intro,
so you no longer need to fold them into `index_intro` by hand.
Then `write_file('$SESSION_DIR/okf-input.json', <json>)`.

## Step 5 — serialize

Call `okf.build` with:
- `script = $SESSION_DIR/build_bundle.py`
- `input  = $SESSION_DIR/okf-input.json`
- `output = $SESSION_DIR/okf-bundle`

It writes the bundle tree + `index.md` + `log.md`, applies the strip whitelist,
and returns a JSON report.

## Step 6 — surface the report

Show the user: page count, `type` histogram, `conformant` (true/false),
`violations`, and `broken_links` (broken links are allowed by OKF — report, don't
fail). If `conformant` is false, fix the offending page input (usually a missing
`type` or unterminated frontmatter) and re-run Step 5. Do not hand over a
non-conformant bundle.

## Step 7 — record a receipt

`brain_put_page('okf/exports/<ISO-timestamp>', <markdown summarizing what was
exported: slug count, types, bundle path, conformant flag>)`. This page is
protected user data.

## Step 8 — optional archive

If the user wants a single shippable file, call `okf.pack` with
`input = $SESSION_DIR/okf-bundle`, `output = $SESSION_DIR/okf-bundle.tar.gz`.
Publishing to git is left to the user (a network side-effect); print the bundle
path and a short `git init && git add . && git commit && git remote add && git push`
checklist rather than performing it.
