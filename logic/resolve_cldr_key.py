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

def resolve_cldr_key(lang_id: str, iso_info: dict) -> str:
    """
    CLDR käyttää ISO-639-1 koodeja aina kun mahdollista.
    Jos kieli on ISO-639-3 (esim. 'fin') ja sillä on iso639_1 ('fi'),
    käytetään CLDR-hakuihin iso639_1-koodia.
    """
    iso1 = iso_info.get("iso639_1")
    if iso1:
        return iso1
    return lang_id

