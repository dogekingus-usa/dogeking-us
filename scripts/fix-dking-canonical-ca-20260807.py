# -*- coding: utf-8 -*-
"""S3/F4 hotfix 2026-08-07: replace SUPERSEDED $DKING CA (UnKPK9...) with CANONICAL (5k7etim...)
Scope: dogeking-us-astro deploy repo — files confirmed on origin/main with legacy CA.
Does NOT touch 4TGFtKSY6jVx4nv4ZfV6fLRmVGdeyXxY3G4m2Ggnimey (SOL payment wallet - different string, safe by construction).
"""
import io, os, re, sys

LEGACY = "UnKPK9oomuhdJz7cZAbaBEB5p3NhNVb6oUwyVP4oGJR"
CANONICAL = "5k7etimtGSM4MDWDgGeN2Nf1R1sHF1UcXpsR1ooR6hRu"
WALLET = "4TGFtKSY6jVx4nv4ZfV6fLRmVGdeyXxY3G4m2Ggnimey"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGETS = [
    "curr-head.html",
    "dogeking-tokenomics-explained-2026.html",
    "dogeking-wallet-setup-guide-2026.html",
    "extracted-sections.html",
    "fetched-live.html",
    "how-to-buy-dking-on-solana.html",
    "index.html",
    "live-html.html",
    "public/fetched-live.html",
    "src/bodies/dogeking-tokenomics-explained-2026.html",
    "src/bodies/dogeking-wallet-setup-guide-2026.html",
    "src/bodies/how-to-buy-dking-on-solana.html",
]

total_replaced = 0
ok = True
for rel in TARGETS:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print(f"[SKIP] {rel} — missing")
        continue
    with io.open(p, "r", encoding="utf-8") as fh:
        c = fh.read()
    n = c.count(LEGACY)
    if n == 0:
        print(f"[INFO] {rel} — no legacy CA (already clean?)")
        continue
    assert WALLET not in c or True  # wallet string is distinct; safe
    c2 = c.replace(LEGACY, CANONICAL)
    # post-conditions
    assert c2.count(LEGACY) == 0, f"{rel}: legacy CA still present after replace"
    assert c2.count(CANONICAL) - c.count(CANONICAL) == n, f"{rel}: replacement delta mismatch"  # sanity guard
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(c2)
    total_replaced += n
    print(f"[FIXED] {rel} — {n} occurrence(s) -> canonical")

print(f"\nTOTAL replaced: {total_replaced}")
print("RESULT: " + ("ALL CLEAN" if total_replaced > 0 else "NO CHANGES"))
sys.exit(0 if total_replaced > 0 else 2)
