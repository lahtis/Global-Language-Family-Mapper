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

import sys
import urllib.request
from pathlib import Path
from parse_iso_files import parse_all_iso_files


DATA = Path("data")
DATA.mkdir(exist_ok=True)

URLS = {
    "iso_639_3": "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab",
    "iso_639_3_names": "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Name_Index.tab",
    "iso_639_3_macrolanguages": "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3-macrolanguages.tab",
    "iso_639_5": "https://id.loc.gov/vocabulary/iso639-5.skos.rdf",
}


def fail(msg):
    print("\nFATAL ERROR:", msg)
    sys.exit(1)


def safe_download(url_key):
    url = URLS[url_key]
    out = DATA / f"{url_key}.tab" if url_key != "iso_639_5" else DATA / f"{url_key}.rdf"

    print(f"Ladataan {url_key}: {url}")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                fail(f"HTTP {response.status} ladattaessa {url_key}")
            content = response.read().decode("utf-8")
    except Exception as e:
        fail(f"Virhe ladattaessa {url_key}: {e}")

    try:
        out.write_text(content, encoding="utf-8")
    except Exception as e:
        fail(f"Virhe tallennettaessa {out}: {e}")

    print(f"Tallennettu: {out}")
    return out


def generate_iso_modules():
    print("\n=== Ladataan ISO-lähteet ===")

    tab3 = safe_download("iso_639_3")
    tab_names = safe_download("iso_639_3_names")
    tab_macro = safe_download("iso_639_3_macrolanguages")
    rdf5 = safe_download("iso_639_5")

    print("\n=== Parsitaan ISO-tiedostot (parse_iso_files.py) ===")

    data = parse_all_iso_files(
        tab3,
        tab_names,
        tab_macro,
        rdf5,
    )

    print("\n=== Kirjoitetaan Python-moduulit data/-hakemistoon ===")

    try:
        (DATA / "iso_639_1.py").write_text(
            f"iso_639_1 = {data['iso639_1']}\n", encoding="utf-8"
        )
        (DATA / "iso_639_2.py").write_text(
            f"iso_639_2 = {data['iso639_2']}\n", encoding="utf-8"
        )
        (DATA / "iso_639_3.py").write_text(
            f"iso_639_3 = {data['iso639_3']}\n", encoding="utf-8"
        )
        (DATA / "iso_639_3_names.py").write_text(
            f"iso_639_3_names = {data['iso639_3_names']}\n", encoding="utf-8"
        )
        (DATA / "iso_639_3_macrolanguages.py").write_text(
            f"iso_639_3_macrolanguages = {data['iso639_3_macrolanguages']}\n",
            encoding="utf-8"
        )
        (DATA / "iso_639_5.py").write_text(
            f"iso_639_5 = {data['iso639_5']}\n", encoding="utf-8"
        )

    except Exception as e:
        fail(f"Virhe kirjoitettaessa Python-moduuleja: {e}")

    print("\nKaikki ISO-moduulit generoitu onnistuneesti data/-hakemistoon.")


if __name__ == "__main__":
    generate_iso_modules()

