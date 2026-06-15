# okf-export-pack

A [NevoFlux](https://github.com/dorisgyl/nevoflux) pack (`pack-protocol/0.1`) that
exports your GBrain knowledge as a conformant **Open Knowledge Format (OKF) v0.1**
bundle — one of the first independent OKF producers outside Google.

## What is OKF?

The **Open Knowledge Format** is a universal, vendor-neutral format for
representing knowledge as plain Markdown files with YAML frontmatter. It is
designed so that *anyone* can produce it (people, agents, export pipelines) and
*anything* can consume it (file servers, knowledge UIs, LLMs, search indexes,
graph viewers) — with no SDK or proprietary API in between.

- Spec & rationale:
  <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md>
- Background (Google Cloud):
  <https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing>

An OKF **bundle** is a directory of Markdown files:

- **Concepts** — every non-reserved `.md` is one concept. It opens with a YAML
  frontmatter block, and `type` is required (e.g. `Spec`, `Note`, `Concept`).
  The file path is the concept ID (`a/b/c.md` → `a/b/c`).
- **`index.md`** (bundle root) — the table of contents; its frontmatter carries
  only `okf_version`.
- **`log.md`** — a dated changelog, `## YYYY-MM-DD` sections, newest first.
- **Links** are bundle-relative (`/a/b.md`). Links are *untyped* — the kind of
  relationship is conveyed by the surrounding prose, not the link itself.
- **Extension keys** (e.g. `x-confidence`) are tolerated; unknown frontmatter is
  ignored by consumers.

## Why OKF?

- **Human- and agent-readable** — no SDK or query language stands between a
  reader and the content; it is just Markdown.
- **Version-controllable out of the box** — bundles live in git, so line-by-line
  diffs, blame, and pull-request review just work.
- **Portable and lock-in free** — a bundle is a directory of files; no
  proprietary API stands between you and your knowledge.
- **Structured *and* unstructured, deliberately** — YAML frontmatter for
  queryable fields, Markdown body for prose, in the same file.
- **Graph-shaped, not just tree-shaped** — links express relationships across
  the whole bundle, not only parent/child folders.

Typical uses: cataloging metadata from data sources into browsable bundles,
publishing or archiving a knowledge base as plain files, and feeding downstream
consumers (RAG pipelines, wikis, static sites, graph viewers) a predictable,
well-typed structure.

## What this pack does

- Projects a selection of GBrain pages into a conformant **OKF v0.1 bundle
  directory** (concepts + `index.md` + `log.md`).
- **Deterministic** serialization: a stdlib-only Python serializer does the
  projection and **self-validates** the output, reporting `conformant`,
  `violations`, and `broken_links` (broken links are allowed by OKF — reported,
  never fatal).
- **Privacy enforced in code, not by prompt**: include only chosen
  prefixes/tags, drop excluded prefixes (e.g. `private/`, `.raw/`), and keep only
  whitelisted frontmatter keys. The boundary is the script, so the same pack is
  safe pointed at real personal memory.
- Optionally **packs the bundle into a single `.tar.gz`** for publishing.

### Components it ships

- **`okf-export` skill** — orchestrates selection → fetch → serialize → report.
- **`okf` host skill** — mapping / conformance / privacy conventions + the serializer.
- **`okf.build` / `okf.pack` canvas-tools** — run the serializer / archive the bundle.
- **`okf/export-config` seed page** — a single, user-editable export config.

## Install

```bash
nevoflux pack validate okf-export-pack/pack.toml
nevoflux pack install  okf-export-pack/pack.toml
```

## Usage

1. **Configure what to export.** Edit the `okf/export-config` page (seeded on
   install) — it is the single source of truth for scope and privacy:
   - `include_prefixes` / `include_tags` — what to include;
   - `exclude_prefixes` — what to always drop (defaults: `private/`, `.raw/`);
   - `frontmatter_whitelist` — which frontmatter keys survive into the bundle
     (`type` is always kept);
   - `bundle_title` / `bundle_description` / `okf_version` — bundle metadata.
2. **Run the `okf-export` skill.** It resolves the page selection, builds the
   bundle, and surfaces a report: page count, `type` histogram, `conformant`
   (true/false), `violations`, and `broken_links`.
3. **(optional) Archive.** Ask it to pack the bundle into a `.tar.gz` you can
   commit or publish.

The export config is a normal, protected GBrain page: edit it any time, and your
edits survive pack updates and uninstall (only `--purge-data` removes them).

### Try the serializer standalone

```bash
python3 components/skills/okf/scripts/build_bundle.py \
  --input tests/fixtures/okf-input.json --output /tmp/okf-out
python3 components/skills/okf/scripts/build_bundle.py --check-only /tmp/okf-out
```

## Conformance & conventions

The rules this pack maps to and enforces live alongside the `okf` skill:

- `components/skills/okf/conventions/conformance.md` — OKF v0.1 conformance rules.
- `components/skills/okf/conventions/mapping.md` — GBrain → OKF field mapping.
- `components/skills/okf/conventions/privacy.md` — strip / whitelist rules.

## Scope

Export only. Importing external OKF (ingesting bundles back into GBrain) is out
of scope for v0.1.
