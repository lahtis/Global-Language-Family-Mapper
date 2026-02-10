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
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"

# Input options
LANGUOIDS_JSON = DATA_ROOT / "languoids.json"
LANGUOIDS_TREE = DATA_ROOT / "languoids" / "tree"

# Output
OUTPUT = DATA_ROOT / "glottolog.json"


def load_from_languoids_json():
    """
    Jos käytössä on valmiiksi koottu languoids.json (helppo tapa).
    """
    with open(LANGUOIDS_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    result = {}

    for entry in raw:
        code = entry.get("id")
        if not code:
            continue

        result[code] = {
            "macroarea": entry.get("macroarea"),
            "latitude": entry.get("latitude"),
            "longitude": entry.get("longitude"),
            "lineage": entry.get("lineage", []),
            "family": entry.get("family"),
        }

    return result


def load_from_tree():
    """
    Jos käytössä on Glottologin raakapuuhakemisto languoids/tree/.
    Tämä lukee jokaisen md.ini -tiedoston ja poimii:
    - glottocode
    - macroarea
    - latitude, longitude
    - family lineage
    """

    result = {}

    for root, dirs, files in os.walk(LANGUOIDS_TREE):
        if "md.ini" not in files:
            continue

        md_path = Path(root) / "md.ini"

        glotto = {}
        code = None

        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line.startswith("id ="):
                    code = line.split("=", 1)[1].strip()

                elif line.startswith("macroarea ="):
                    glotto["macroarea"] = line.split("=", 1)[1].strip()

                elif line.startswith("latitude ="):
                    try:
                        glotto["latitude"] = float(line.split("=", 1)[1].strip())
                    except:
                        glotto["latitude"] = None

                elif line.startswith("longitude ="):
                    try:
                        glotto["longitude"] = float(line.split("=", 1)[1].strip())
                    except:
                        glotto["longitude"] = None

                elif line.startswith("family ="):
                    glotto["family"] = line.split("=", 1)[1].strip()

                elif line.startswith("lineage ="):
                    lineage = line.split("=", 1)[1].strip()
                    glotto["lineage"] = [x.strip() for x in lineage.split(",")]

        if code:
            result[code] = {
                "macroarea": glotto.get("macroarea"),
                "latitude": glotto.get("latitude"),
                "longitude": glotto.get("longitude"),
                "lineage": glotto.get("lineage", []),
                "family": glotto.get("family"),
            }

    return result


def build_glottolog():
    """
    Valitsee automaattisesti oikean lähteen ja tuottaa glottolog.json.
    """

    if LANGUOIDS_JSON.exists():
        print("Using languoids.json as source...")
        data = load_from_languoids_json()

    elif LANGUOIDS_TREE.exists():
        print("Using languoids/tree/ as source...")
        data = load_from_tree()

    else:
        raise FileNotFoundError(
            "No Glottolog source found. Expected languoids.json or languoids/tree/"
        )

    print(f"Saving glottolog.json → {OUTPUT}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Done.")


if __name__ == "__main__":
    build_glottolog()

