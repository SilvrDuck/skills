#!/usr/bin/env python3
"""align-check <symbol>  < block
Verify a symbol lands at identical display columns on every line that contains it.
Exit 0 + "OK" if aligned; exit 1 + per-signature line list if it drifts.
Stdlib only.
"""
import sys, unicodedata

def width(s):
    """Display width to Unicode spec: Wide/Fullwidth and emoji = 2, FE0F widens
    its base, combining marks / ZWJ / format = 0, everything else = 1."""
    chars = list(s)
    w = 0
    for i, ch in enumerate(chars):
        if ord(ch) == 0xFE0F:                                   # emoji selector
            continue
        if unicodedata.category(ch) in ("Mn", "Me", "Cf"):      # combining/ZWJ/format
            continue
        if unicodedata.east_asian_width(ch) in ("W", "F"):      # wide / fullwidth
            w += 2
        elif i + 1 < len(chars) and ord(chars[i + 1]) == 0xFE0F:  # forced emoji
            w += 2
        else:
            w += 1
    return w

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: align-check <symbol> < block")
    sym = sys.argv[1]
    # force UTF-8 I/O so it behaves the same on Windows consoles
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    order, lines = [], {}
    for n, line in enumerate(sys.stdin, 1):
        line = line.rstrip("\n")
        sig, frm = [], 0
        while (idx := line.find(sym, frm)) >= 0:
            sig.append(width(line[:idx]) + 1)        # 1-based display column
            frm = idx + len(sym)
        if not sig:
            continue
        key = ",".join(map(str, sig))
        if key not in lines:
            order.append(key)
            lines[key] = []
        lines[key].append(n)

    if len(order) <= 1:
        print("OK")
        sys.exit(0)
    print(f'DRIFT "{sym}": {len(order)} distinct column signatures')
    for k in order:
        print(f"  cols[{k}] <- lines {' '.join(map(str, lines[k]))}")
    sys.exit(1)

if __name__ == "__main__":
    main()
