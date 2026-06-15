# OKF v0.1 conformance (what this pack guarantees)

A bundle is conformant if (§9):
1. every non-reserved `.md` has a parseable YAML frontmatter block;
2. every frontmatter block has a non-empty `type`;
3. reserved filenames (`index.md`, `log.md`) follow §6/§7.

Reserved-filename rules:
- `index.md` carries NO frontmatter, EXCEPT the bundle-root `index.md`, which may
  carry only `okf_version` (§6/§11).
- `log.md` is `## YYYY-MM-DD` date sections, newest first; leading bold word
  (`**Creation**`/`**Update**`) is a convention (§7).

Links (§5): bundle-relative absolute (`/x.md`) preferred; broken links are
TOLERATED (report, never fail).

`build_bundle.py` self-checks the output against §9 rules 1–3 and the
reserved-filename rules above — root `index.md` frontmatter must carry
`okf_version` and nothing else (§11), and `log.md` sections must be
`## YYYY-MM-DD` dates in newest-first order (§7) — reporting
`{ conformant, violations, broken_links }`. The bold leading word in `log.md`
entries is a convention and is not enforced. Never ship a bundle with
`conformant: false`.
