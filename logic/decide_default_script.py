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

def decide_default_script(lang_id, wikt, cldr, written, iso_info):
    """
    Päätetään oletusskripti:
    1. written-languages → ensimmäinen tunnettu script
    2. CLDR likelySubtags → script
    3. Wiktionary → ensimmäinen tunnettu script
    4. fallback: 'Latn'
    """

    # 1. Written-languages
    if written and written.get("scripts"):
        for s in written["scripts"]:
            if s and s.upper() != "UNKNOWN":
                return s

    # 2. CLDR
    cldr_key = iso_info.get("iso639_1", lang_id)
    if cldr_key in cldr:
        tag = cldr[cldr_key]
        if isinstance(tag, str):
            parts = tag.split("-")  # huom! CLDR käyttää '-'
            if len(parts) >= 2:
                return parts[1]

    # 3. Wiktionary
    if wikt and wikt.get("scripts"):
        for s in wikt["scripts"]:
            if s and s.upper() != "UNKNOWN":
                return s

    # 4. fallback
    return "Latn"

