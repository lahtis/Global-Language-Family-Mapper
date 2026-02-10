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

from typing import Dict, Any

# Lue generate_iso_files.py:n tuottamat Python-moduulit
from data.iso_639_1 import iso_639_1
from data.iso_639_2 import iso_639_2
from data.iso_639_3 import iso_639_3
from data.iso_639_5 import iso_639_5
from data.iso_639_3_names import iso_639_3_names
from data.iso_639_3_macrolanguages import iso_639_3_macrolanguages


def _safe(obj, key, default=""):
    """Turvallinen .get() joka ei kaadu jos obj ei ole dict."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return default


def load_iso_639() -> Dict[str, Any]:
    unified: Dict[str, Any] = {}

    # --- ISO 639‑3: peruskielet ---
    for code3, info3 in iso_639_3.items():
        unified[code3] = {
            "name": _safe(info3, "name", code3),
            "iso639_1": _safe(info3, "iso639_1", ""),
            "iso639_2B": _safe(info3, "iso639_2B", ""),
            "iso639_2T": _safe(info3, "iso639_2T", ""),
            "iso639_3": code3,
            "iso639_5": "",
            "aliases": iso_639_3_names.get(code3, []),
            "macrolanguages": iso_639_3_macrolanguages.get(code3, []),
        }

    # --- ISO 639‑2: varmista 2-koodit ---
    for code3, info2 in iso_639_2.items():
        if code3 in unified:
            unified[code3]["iso639_2B"] = _safe(info2, "iso639_2B", unified[code3]["iso639_2B"])
            unified[code3]["iso639_2T"] = _safe(info2, "iso639_2T", unified[code3]["iso639_2T"])

    # --- ISO 639‑1: varmista 1-koodit ---
    for code1, info1 in iso_639_1.items():

        # info1 voi olla string TAI dict → käsitellään molemmat
        if isinstance(info1, dict):
            code3 = info1.get("iso639_3")
        else:
            # jos info1 on string, generate_iso_files.py EI antanut iso639_3-kenttää
            # → ei voida yhdistää 1-koodia 3-koodiin
            continue

        if code3 and code3 in unified:
            unified[code3]["iso639_1"] = code1

    # --- ISO 639‑5: kieliperheet ---
    for family_code, info5 in iso_639_5.items():
        name = _safe(info5, "name", family_code)
        unified[family_code] = {
            "name": name,
            "iso639_1": "",
            "iso639_2B": "",
            "iso639_2T": "",
            "iso639_3": "",
            "iso639_5": family_code,
            "aliases": [],
            "macrolanguages": [],
        }

    return unified

