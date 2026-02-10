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

import json
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLDR_ROOT = PROJECT_ROOT / "data" / "cldr"
CLDR_ROOT.mkdir(parents=True, exist_ok=True)

LOCAL_FILE = CLDR_ROOT / "likelySubtags.json"

# Virallinen CLDR-likelySubtags.json (Unicode Consortium)
CLDR_URL = (
    "https://raw.githubusercontent.com/unicode-org/cldr-json/"
    "master/cldr-json/cldr-core/supplemental/likelySubtags.json"
)


def download_cldr_likely_subtags():
    """Lataa virallisen CLDR-likelySubtags.json-tiedoston."""
    try:
        print("Downloading CLDR likelySubtags.json from Unicode CLDR...")
        with urllib.request.urlopen(CLDR_URL) as response:
            data = response.read().decode("utf-8")

        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            f.write(data)

        print("CLDR likelySubtags.json downloaded successfully.")

    except Exception as e:
        print("Failed to download CLDR likelySubtags.json:", e)


def load_cldr_likely_subtags():
    """
    Lataa CLDR-likelySubtags-tiedoston.
    Jos tiedostoa ei ole, lataa se automaattisesti Unicode CLDR:stä.
    Palauttaa standardinmukaisen dictin: { "fi": "fi_Latn_FI", ... }
    """
    if not LOCAL_FILE.exists():
        download_cldr_likely_subtags()

    if not LOCAL_FILE.exists():
        return {}

    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # CLDR-rakenne: {"supplemental": {"likelySubtags": {...}}}
    return raw.get("supplemental", {}).get("likelySubtags", {})

