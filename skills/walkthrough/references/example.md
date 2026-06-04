# walkthrough — a fully-formed stop

One complete stop, assembling every section from the Visual kit in SKILL.md.
Read this before your first stop so your rendering matches.

The unit here is a pipeline stage; swap it for whatever the project's step unit
is. The shape stays the same.

````
╔══════════════════════════════════════════════════════════════════════════════╗
║   ▶  STOP 2 / 4   ·   normalize_row()   ·   coerce a raw row into a typed Record ║
║      📄 pipeline/ingest.py:61                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────  🗺️  minimap  ──────────────────────────────────────
Source CSV ─→ parse ─→ [normalize_row] ─→ validate ─→ warehouse
                        ^^^^^^^^^^^^^^^^
                        coerce types, fill defaults

──────────────────────────────────  🧠 what it does  ──────────────────────────────────
The first stage that can fail on *data*, not format. Upstream `parse` only split
the columns; here each string becomes its real type and missing optionals get
defaults — so every stage after this can assume a clean `Record` and stop
defending against raw strings.

```python
def normalize_row(raw: dict[str, str]) -> Record:
    return Record(
        id=int(raw["id"]),                     # ← values arrive as strings from the CSV reader
        email=raw["email"].strip().lower(),    # ← canonical form, set once, here
        signup=parse_date(raw.get("signup")),  # ← None when absent, never ""
    )
```

──────────────────────────────────────  🧳 data panel  ──────────────────────────────────────
INPUT (raw, all strings)                 →   OUTPUT (typed Record)
{ "id": "42",                                Record(id=42,
  "email": " Ada@X.io ",                              email="ada@x.io",   ◀── trimmed + lowercased
  "signup": "" }                                      signup=None)        ◀── "" → None

──────────────────────────────────────  🎛️  controls  ──────────────────────────────────────
- [n] next — Stop 3: validate() rejects records that violate the schema.
- [s] step into — parse_date(): how blank or garbage dates become None.
- [b] back — Stop 1 (the CSV reader).
- or ask anything inline.
╚══════════════════════════════ end stop 2 ═══════════════════════════════════╝
````
