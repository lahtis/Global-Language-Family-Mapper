#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Tuomas Lähteenmäki
#
# Licensed under the MIT License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import time
import requests
from pathlib import Path
from collections import defaultdict

# --- Project root ---
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Paths ---
CODE_TO_QID = ROOT_DIR / "maps" / "code_to_family_qid.json"
CACHE_PARENTS = ROOT_DIR / "cache" / "cache_qid_to_parents.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_parent_chain.json"

# --- Wikidata API ---
API = "https://www.wikidata.org/w/api.php"
HEADERS = {"User-Agent": "TuomasParentBot/1.0"}

# --- Helpers ---

def safe_get(url, params):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return r.json()
    except Exception as e:
        print("DEBUG safe_get error:", e)
        return None

def load_cache(path):
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_parents(qid):
    params = {
        "action": "wbgetclaims",
        "entity": qid,
        "format": "json"
    }
    data = safe_get(API, params)
    parents = set()
    if data and "claims" in data:
        for prop in ("P279", "P361"):  # subclass of, part of
            for claim in data["claims"].get(prop, []):
                try:
                    pid = claim["mainsnak"]["datavalue"]["value"]["id"]
                    parents.add(pid)
                except:
                    pass
    return list(parents)

# --- Main ---

def main():
    print("--- BUILD PARENT CHAINS ---")

    if not CODE_TO_QID.exists():
        print(f"ERROR: {CODE_TO_QID} missing.")
        return

    code_to_qid = json.load(CODE_TO_QID.open("r", encoding="utf-8"))
    parent_cache = load_cache(CACHE_PARENTS)
    code_to_chain = {}

    total = len(code_to_qid)
    for i, (code, qid) in enumerate(code_to_qid.items(), 1):
        pct = (i / total) * 100
        print(f"\r[{pct:5.1f}%] Processing {code} -> {qid}", end="", flush=True)

        if not qid:
            code_to_chain[code] = []
            continue

        if qid in parent_cache:
            code_to_chain[code] = parent_cache[qid]
            continue

        chain = []
        visited = set()
        current = qid
        while current and current not in visited:
            visited.add(current)
            parents = fetch_parents(current)
            if not parents:
                break
            current = parents[0]
            chain.append(current)
            parent_cache[current] = parents

        code_to_chain[code] = chain

        # Save cache periodically
        if i % 20 == 0:
            save_cache(CACHE_PARENTS, parent_cache)

        time.sleep(0.1)  # rate limiting

    # Save final caches
    save_cache(CACHE_PARENTS, parent_cache)
    save_cache(OUTPUT, code_to_chain)

    print(f"\nDONE: {OUTPUT}")

if __name__ == "__main__":
    main()

