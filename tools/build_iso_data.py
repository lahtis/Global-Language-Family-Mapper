#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# GLFM Project
# Copyright (c) 2026 Tuomas Lähteenmäki
#
# https://codeberg.org/lahtis/GLFM
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

import csv
import json
from pathlib import Path
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"

# Output files
ISO1_OUT = DATA_ROOT / "iso_639_1.json"
ISO2_OUT = DATA_ROOT / "iso_639_2.json"
ISO3_OUT = DATA_ROOT / "iso_639_3.json"

# Official ISO sources
ISO_639_3_URL = "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab"
ISO_639_2_URL = "https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt"
ISO_639_1_URL = "https://datahub.io/core/language-codes/r/language-codes.csv"


def download(url: str, path: Path):
    """
    Download with User-Agent and fallback mirror for ISO-639-3.
    """
    print(f"Downloading {url} ...")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            path.write_bytes(data)
            print(f"Saved to {path}")
            return
    except Exception as e:
        print(f"Primary download failed: {e}")

    # Fallback mirror for ISO-639-3
    if "iso-639-3.tab" in url:
        fallback_url = (
            "https://raw.githubusercontent.com/haliaeetus/iso-639/master/data/iso-639-3.tab"
        )
        print(f"Trying fallback mirror: {fallback_url}")

        req2 = urllib.request.Request(
            fallback_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req2) as response:
            data = response.read()
            path.write_bytes(data)
            print(f"Saved from fallback mirror to {path}")
            return

    raise RuntimeError(f"Failed to download {url}")


def build_iso_639_3():
    """
    Builds iso_639_3.json from SIL's official iso-639-3.tab file.
    Handles both old and new column names.
    """
    tmp = DATA_ROOT / "iso-639-3.tab"
    download(ISO_639_3_URL, tmp)

    iso3 = {}

    with open(tmp, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code3 = row["Id"]

            # Handle both old and new column names
            iso2B = row.get("Part2_B") or row.get("Part2B") or ""
            iso2T = row.get("Part2_T") or row.get("Part2T") or ""
            iso1 = row.get("Part1") or ""

            iso3[code3] = {
                "name": row.get("Ref_Name", ""),
                "iso639_3": code3,
                "iso639_2B": iso2B,
                "iso639_2T": iso2T,
                "iso639_1": iso1,
                "iso639_5": "",
            }

    ISO3_OUT.write_text(json.dumps(iso3, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {ISO3_OUT}")


def build_iso_639_2():
    """
    Builds iso_639_2.json from Library of Congress ISO-639-2 list.
    """
    tmp = DATA_ROOT / "iso-639-2.txt"
    download(ISO_639_2_URL, tmp)

    iso2 = {}

    with open(tmp, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) < 4:
                continue

            code2B, code2T, code1, name = parts[:4]

            iso2[code2T] = {
                "name": name,
                "iso639_2B": code2B,
                "iso639_2T": code2T,
                "iso639_1": code1,
                "iso639_3": "",
            }

    ISO2_OUT.write_text(json.dumps(iso2, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {ISO2_OUT}")


def build_iso_639_1():
    """
    Builds iso_639_1.json from DataHub language-codes.csv.
    Handles multiple possible column names.
    """
    tmp = DATA_ROOT / "language-codes.csv"
    download(ISO_639_1_URL, tmp)

    iso1 = {}

    with open(tmp, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Possible column names
            code1 = row.get("alpha2") or row.get("Alpha2") or row.get("ISO639-1")
            code3 = (
                row.get("alpha3-b")
                or row.get("alpha3")
                or row.get("Alpha3")
                or row.get("ISO639-2B")
                or row.get("ISO639-3")
            )
            name = row.get("English") or row.get("Name") or row.get("name")

            if not code1:
                continue

            iso1[code1] = {
                "name": name or "",
                "iso639_1": code1,
                "iso639_3": code3 or "",
            }

    ISO1_OUT.write_text(json.dumps(iso1, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {ISO1_OUT}")


def main():
    print("=== Building ISO 639 data ===")
    build_iso_639_3()
    build_iso_639_2()
    build_iso_639_1()
    print("=== ISO data build complete ===")


if __name__ == "__main__":
    main()

