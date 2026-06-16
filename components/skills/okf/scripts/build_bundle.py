#!/usr/bin/env python3
"""build_bundle.py — deterministic GBrain-JSON -> OKF v0.1 bundle serializer.

Shipped inside okf-export-pack (host skill `okf`). The worker writes a verbatim
copy to $SESSION_DIR, then a canvas-tool runs:

    python3 build_bundle.py --input okf-input.json --output okf-bundle/

It also validates an existing bundle:

    python3 build_bundle.py --check-only okf-bundle/

stdlib-only (no pyyaml): frontmatter is hand-emitted and the conformance gate
scans for a non-empty `type:` line rather than full-parsing YAML, so it stays
dependency-free and robust against bundles authored elsewhere.

Reads nothing from the network and writes only under --output.
"""
import argparse, json, os, re, sys, pathlib

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\]\((/[^)]+\.md)\)")          # bundle-relative links: ](/x.md)
TYPE_RE = re.compile(r"^type:\s*\"?([^\"\n]+?)\"?\s*$", re.M)
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):", re.M)     # frontmatter key lines (§11 exclusivity)
LOG_HDR_RE = re.compile(r"^##(?!#)\s*(.+?)\s*$", re.M)  # log.md level-2 section headers (§7)
ISO_DATE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")  # YYYY-MM-DD (§7)

# ----------------------------------------------------------------- emit -----
def yaml_scalar(v):
    if isinstance(v, list):
        return "[" + ", ".join(yaml_scalar(x) for x in v) + "]"
    s = str(v)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def emit_frontmatter(d):
    return "---\n" + "".join(f"{k}: {yaml_scalar(v)}\n" for k, v in d.items()) + "---\n"

def apply_strip(fm, whitelist):
    if not whitelist:
        return fm
    keep = set(whitelist) | {"type"}            # type is mandatory, never stripped
    return {k: v for k, v in fm.items() if k in keep}

def render_page(page, whitelist):
    fm = {"type": page.get("type") or "Concept"}   # non-empty type guaranteed
    for k in ("title", "description", "resource", "tags", "timestamp"):
        if page.get(k):
            fm[k] = page[k]
    for k, v in (page.get("extra") or {}).items():  # producer extensions (§4.1)
        fm[k] = v
    fm = apply_strip(fm, whitelist)
    fm["type"] = page.get("type") or "Concept"      # re-assert after strip
    out = emit_frontmatter(fm) + "\n"
    body = (page.get("body") or "").strip()
    if body:
        out += body + "\n"
    cites = page.get("citations") or []
    if cites:
        out += "\n# Citations\n" + "".join(
            f"[{i}] [{t}]({u})\n" for i, (t, u) in enumerate(cites, 1))
    return out

def render_index(bundle, pages):
    bundle = bundle or {}
    okf_version = bundle.get("okf_version", "0.1")
    # bundle_title/bundle_description come straight from the export-config page;
    # index_intro stays as the most-specific override and wins when both are set.
    heading = bundle.get("bundle_title") or "Index"
    intro = (bundle.get("index_intro") or bundle.get("bundle_description")
             or "Index of this OKF bundle.")
    out = f'---\nokf_version: "{okf_version}"\n---\n\n# {heading}\n\n{intro}\n'
    sections = bundle.get("index_sections")
    if not sections:                                # deterministic fallback: group by type
        by_type = {}
        for p in pages:
            by_type.setdefault(p.get("type") or "Concept", []).append(p)
        sections = [
            {"heading": t, "items": [
                {"title": p.get("title") or p["slug"],
                 "target": "/" + p["slug"] + ".md",
                 "desc": p.get("description", "")} for p in ps]}
            for t, ps in sorted(by_type.items())]
    for sec in sections:
        out += f"\n# {sec['heading']}\n"
        for it in sec["items"]:
            d = f" - {it['desc']}" if it.get("desc") else ""
            out += f"* [{it['title']}]({it['target']}){d}\n"
    return out

def render_log(log):
    out = "# Update log\n"
    for day in log or []:
        out += f"\n## {day['date']}\n"
        for e in day.get("entries", []):
            kind = e.get("kind")
            prefix = f"**{kind}**: " if kind else ""
            out += f"* {prefix}{e['text']}\n"
    return out

# --------------------------------------------------------------- produce ----
def produce(data, outroot):
    outroot = pathlib.Path(outroot)
    strip = data.get("strip") or {}
    whitelist = strip.get("frontmatter_whitelist") or []
    excl = tuple(strip.get("exclude_prefixes") or [])
    kept, skipped = [], []
    for page in data.get("pages", []):
        slug = page["slug"]
        if excl and slug.startswith(excl):
            skipped.append(slug)
            continue
        dest = outroot / (slug + ".md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_page(page, whitelist), encoding="utf-8")
        kept.append(page)
    (outroot / "index.md").write_text(render_index(data.get("bundle"), kept), encoding="utf-8")
    if data.get("log"):
        (outroot / "log.md").write_text(render_log(data["log"]), encoding="utf-8")
    return {"written": len(kept), "skipped_by_strip": skipped}

# ----------------------------------------------------------------- check ----
def check(root):
    root = pathlib.Path(root)
    md = sorted(p for p in root.rglob("*.md"))
    # as_posix(): bundle links are forward-slash, so normalize paths to match on
    # Windows too (str(...) would yield "a\b.md" and mis-report links as broken).
    present = {p.relative_to(root).as_posix() for p in md}
    violations, types, broken = [], {}, []
    for p in md:
        rel = p.relative_to(root).as_posix()
        name = p.name
        text = p.read_text(encoding="utf-8")
        if name in RESERVED:                        # §6/§7/§11 structural checks
            if name == "index.md":
                is_root = (p.parent == root)
                starts_fm = text.startswith("---")
                if starts_fm and not is_root:
                    violations.append(f"{rel}: index.md must not carry frontmatter (§6)")
                if is_root and starts_fm:           # §11: root index frontmatter is okf_version only
                    keys = KEY_RE.findall(text.split("---", 2)[1])
                    if "okf_version" not in keys:
                        violations.append(f"{rel}: root index.md frontmatter must carry okf_version (§11)")
                    extra = sorted(set(keys) - {"okf_version"})
                    if extra:
                        violations.append(
                            f"{rel}: root index.md frontmatter may only carry okf_version; found {extra} (§11)")
            elif name == "log.md":                  # §7: `## YYYY-MM-DD` sections, newest first
                prev = None
                for m in LOG_HDR_RE.finditer(text):
                    hdr = m.group(1)
                    if not ISO_DATE_RE.match(hdr):
                        violations.append(f"{rel}: log section '## {hdr}' is not a YYYY-MM-DD date (§7)")
                        continue
                    if prev is not None and hdr > prev:  # ISO dates compare lexicographically
                        violations.append(
                            f"{rel}: log dates must be newest-first; '{hdr}' follows '{prev}' (§7)")
                    prev = hdr
            continue
        # §9: parseable frontmatter block with a non-empty type
        if not text.startswith("---"):
            violations.append(f"{rel}: missing frontmatter block (§4.1/§9)")
            continue
        end = text.find("\n---", 3)
        if end == -1:
            violations.append(f"{rel}: unterminated frontmatter block (§4.1)")
            continue
        fm = text[3:end]
        m = TYPE_RE.search(fm)
        if not m or not m.group(1).strip():
            violations.append(f"{rel}: empty or missing `type` (§4.1/§9)")
            continue
        types[m.group(1).strip()] = types.get(m.group(1).strip(), 0) + 1
        for link in LINK_RE.findall(text):          # §5: broken links tolerated, just reported
            target = link.lstrip("/")
            if target not in present:
                broken.append({"in": rel, "link": link})
    return {
        "files": len(md),
        "concepts": sum(types.values()),
        "types": types,
        "conformant": len(violations) == 0,
        "violations": violations,
        "broken_links": broken,
    }

# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input")
    ap.add_argument("--output")
    ap.add_argument("--check-only")
    args = ap.parse_args()
    if args.check_only:
        report = check(args.check_only)
    else:
        if not (args.input and args.output):
            ap.error("--input and --output are required unless --check-only is used")
        data = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
        prod = produce(data, args.output)
        report = check(args.output)
        report["produced"] = prod
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["conformant"] else 1)

if __name__ == "__main__":
    main()
