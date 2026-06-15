# Privacy / strip (enforced in the serializer, not in prompt)

Defaults are privacy-safe. The serializer:
- includes only pages whose slug matches `include_prefixes` / `include_tags`;
- drops any page whose slug starts with an `exclude_prefixes` entry
  (e.g. `.raw/`, `private/`);
- keeps only frontmatter keys in `frontmatter_whitelist` (`type` is always kept);
  anything not whitelisted — including extension keys — is removed.

Because strip runs in `build_bundle.py` (deterministic), the same pack is safe
when pointed at real personal memory: the boundary is code, not a prompt asking
the model to "not leak". To export a richer set, widen the whitelist explicitly.
