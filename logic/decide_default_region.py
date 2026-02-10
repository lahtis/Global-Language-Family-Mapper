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

from logic.resolve_cldr_key import resolve_cldr_key

def decide_default_region(lang_id, wikt, cldr, iso_info):
    """
    Päätetään oletusalue:
    1. CLDR likelySubtags → region (fi-Latn-FI → FI)
    2. Wiktionary → region (jos löytyy ja ei UNKNOWN)
    3. fallback: '001' (World)
    """

    # 1. CLDR
    cldr_key = resolve_cldr_key(lang_id, iso_info)
    if cldr_key in cldr:
        tag = cldr[cldr_key]
        if isinstance(tag, str):
            parts = tag.split("-")  # HUOM! CLDR-data käyttää '-'
            if len(parts) == 3:
                region = parts[2]
                if region and region.upper() != "UNKNOWN":
                    return region

    # 2. Wiktionary
    if wikt and wikt.get("region"):
        region = wikt["region"]
        if region and region.upper() != "UNKNOWN":
            return region

    # 3. fallback
    return "001"

