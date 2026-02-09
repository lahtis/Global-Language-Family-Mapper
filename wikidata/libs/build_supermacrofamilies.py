#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

PARENT_CHAINS = Path("maps/code_to_parent_chain.json")
LABELS = Path("cache/cache_label_to_qid.json")

GENERIC = {
    "Q20162172",  # language family
    "Q34770",     # language
    "Q17376908",  # linguistic entity
    "Q7048977",   # linguistic unit
    "Q18205125"   # grouping
}

def load():
    chains = json.load(open(PARENT_CHAINS, "r", encoding="utf-8"))
    labels = json.load(open(LABELS, "r", encoding="utf-8"))
    return chains, labels

def invert_labels(labels):
    return {v: k for k, v in labels.items()}

def main():
    chains, labels = load()
    qid_to_label = invert_labels(labels)

    freq = Counter()
    ancestors = {}

    for code, chain in chains.items():
        cleaned = [qid for qid in chain if qid not in GENERIC]
        if not cleaned:
            continue
        own = cleaned[0]
        anc = cleaned[1:]
        ancestors[code] = anc
        for q in anc:
            freq[q] += 1

    result = {}

    for code, anc in ancestors.items():
        best = None

        # korkein esivanhempi, joka esiintyy useammalla kuin yhdellä perheellä
        for qid in reversed(anc):
            if freq[qid] > 1 and qid_to_label.get(qid):
                best = qid
                break

        # fallback: korkein esivanhempi, jolla on label
        if not best:
            for qid in reversed(anc):
                if qid_to_label.get(qid):
                    best = qid
                    break

        # viimeinen fallback: perheen oma QID
        if not best:
            best = chains[code][0]

        result[code] = {
            "super_macro_qid": best,
            "super_macro_label": qid_to_label.get(best, "(unknown)"),
            "all_ancestors": [
                {
                    "qid": q,
                    "label": qid_to_label.get(q, "(unknown)")
                }
                for q in anc
            ]
        }

    out = Path("maps/code_to_super_macrofamily_full.json")
    json.dump(result, open(out, "w", encoding="utf-8"), indent=2)
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()

