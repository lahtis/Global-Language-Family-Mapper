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
# Safe Wikidata Macrofamily Builder
# Updates wikidata-query.json if missing, uses caches to avoid re-fetching QIDs/parents
#
import json
import requests
from collections import defaultdict, Counter
from pathlib import Path
import time

# --- FILES ---
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
MAPS_DIR = Path(__file__).resolve().parent.parent / "maps"

IN_FILE = DATA_DIR / "wikidata-query.json"
OUT_FILE = MAPS_DIR / "iso_macrofamily_raw2.json"
CACHE_LABEL = CACHE_DIR / "cache_label_to_qid.json"
CACHE_PARENTS = CACHE_DIR / "cache_qid_to_parents.json"

API = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "User-Agent": "GLFM-MacroFamilyBot/1.0 (https://codeberg.org/lahtis/GLFM; contact: lahtis@gmail.com)"
}

STOP_NODES = {"Q315", "Q33596", "Q25295", "Q34770", "Q1288568", "Q46291", "Q201658"}
SEARCH_VARIANTS = [
    "{label}", "{label} language", "{label} languages",
    "{label} (language)", "{label} (languages)",
    "{label} family", "{label} language family"
]

# --- HELPERS ---
def normalize_label(s):
    return s.strip().replace("\u00A0", " ").replace("\u202F", " ").replace("\u200B", "").replace("&nbsp;", " ")

def safe_get(url, params):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
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

def fetch_wikidata_query():
    """
    Hakee Wikidatasta kaikki ISO 639-3 kielet ja niiden perheet.
    Tallentaa JSON-tiedoston data/wikidata-query.json
    """
    print("Fetching data from Wikidata SPARQL endpoint...")
    url = "https://query.wikidata.org/sparql"
    query = """
    SELECT ?iso ?langLabel ?familyLabel ?subfamilyLabel ?scriptLabel WHERE {
      ?lang wdt:P218 ?iso.
      OPTIONAL { ?lang wdt:P31 ?instance. }
      OPTIONAL { ?lang wdt:P279 ?family. }
      OPTIONAL { ?lang wdt:P171 ?subfamily. }
      OPTIONAL { ?lang wdt:P407 ?script. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """
    headers = {"User-Agent": HEADERS["User-Agent"]}
    r = requests.get(url, params={"query": query, "format": "json"}, headers=headers, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"Wikidata query failed: {r.status_code}")
    data = r.json()
    rows = []
    for item in data.get("results", {}).get("bindings", []):
        row = {}
        row["iso639_3"] = item.get("iso", {}).get("value")
        row["langLabel"] = item.get("langLabel", {}).get("value")
        row["familyLabel"] = item.get("familyLabel", {}).get("value")
        row["subfamilyLabel"] = item.get("subfamilyLabel", {}).get("value")
        row["scriptLabel"] = item.get("scriptLabel", {}).get("value")
        rows.append(row)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with IN_FILE.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved Wikidata query to {IN_FILE}")
    return rows

# --- MAIN LOGIC ---
def search_entity(label, cache):
    label = normalize_label(label)
    if label in cache:
        return cache[label]
    for variant in SEARCH_VARIANTS:
        query = variant.format(label=label)
        params = {"action": "wbsearchentities", "search": query, "language": "en", "format": "json", "limit": 1}
        data = safe_get(API, params)
        if data and data.get("search"):
            qid = data["search"][0]["id"]
            cache[label] = qid
            save_cache(CACHE_LABEL, cache)
            return qid
    cache[label] = None
    save_cache(CACHE_LABEL, cache)
    return None

def get_parents(qid, cache):
    if qid in cache:
        return cache[qid]
    if not qid or qid in STOP_NODES:
        return []
    params = {"action": "wbgetentities", "ids": qid, "format": "json", "props": "claims"}
    data = safe_get(API, params)
    parents = set()
    if data and "entities" in data and qid in data["entities"]:
        claims = data["entities"][qid].get("claims", {})
        for prop in ("P279", "P171", "P361"):
            for c in claims.get(prop, []):
                try:
                    parents.add(c["mainsnak"]["datavalue"]["value"]["id"])
                except:
                    pass
    res = list(parents)
    cache[qid] = res
    save_cache(CACHE_PARENTS, cache)
    return res

def build_full_graph(qid, cache, graph, depth=0, visited=None):
    if visited is None:
        visited = set()
    if not qid or qid in STOP_NODES or depth > 20 or qid in visited:
        return
    visited.add(qid)
    parents = get_parents(qid, cache)
    for p in parents:
        graph[qid].add(p)
        build_full_graph(p, cache, graph, depth + 1, visited)

def climb(qid, graph):
    seen = set()
    cur = qid
    while cur in graph and graph[cur] and cur not in seen:
        seen.add(cur)
        candidates = [p for p in graph[cur] if p not in STOP_NODES]
        if not candidates:
            break
        cur = sorted(candidates)[0]
    return cur

def main():
    print("--- Starting Wikidata Macrofamily Builder ---")

    # Jos tiedosto puuttuu, luodaan se API:lla
    if not IN_FILE.exists():
        print(f"Input {IN_FILE} missing. Attempting to create from Wikidata...")
        try:
            rows = fetch_wikidata_query()
        except Exception as e:
            print(f"ERROR: Failed to fetch Wikidata query: {e}")
            return
    else:
        try:
            with IN_FILE.open("r", encoding="utf-8") as f:
                rows = json.load(f)
        except Exception as e:
            print(f"ERROR reading input file: {e}")
            return

    label_cache = load_cache(CACHE_LABEL)
    parent_cache = load_cache(CACHE_PARENTS)

    iso_to_fams = defaultdict(list)
    all_labels = []

    for r in rows:
        fam = r.get("familyLabel")
        if fam:
            fam = normalize_label(fam)
            all_labels.append(fam)
            iso = r.get("iso639_3")
            if iso:
                iso_to_fams[iso].append(fam)

    all_labels = sorted(set(all_labels))
    total_labels = len(all_labels)
    print(f"Found {total_labels} unique language families. Fetching QIDs...")

    label_to_qid = {}
    for i, fam in enumerate(all_labels, 1):
        pct = (i / total_labels) * 100
        print(f"\r[{pct:5.1f}%] Fetching: {fam[:30]:<30}", end="", flush=True)
        label_to_qid[fam] = search_entity(fam, label_cache)
        time.sleep(0.05)  # hiljentää API:ta

    print("\nQID fetching complete. Building full parent graph...")

    graph = defaultdict(set)
    for i, (fam, qid) in enumerate(label_to_qid.items(), 1):
        if qid:
            pct = (i / len(label_to_qid)) * 100
            print(f"\r[{pct:5.1f}%] Processing graph: {qid:<10}", end="", flush=True)
            build_full_graph(qid, parent_cache, graph)
            time.sleep(0.01)

    print("\nFinalizing results and computing macrofamilies...")
    iso_macro = {}
    for iso, fams in iso_to_fams.items():
        roots = [climb(label_to_qid[f], graph) for f in fams if label_to_qid.get(f)]
        iso_macro[iso] = Counter(roots).most_common(1)[0][0] if roots else "Unknown"

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(iso_macro, f, ensure_ascii=False, indent=2)

    print(f"\nAll done! Saved: {OUT_FILE}")

if __name__ == "__main__":
    main()

