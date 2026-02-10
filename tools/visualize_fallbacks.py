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
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIFIED = PROJECT_ROOT / "output" / "unified" / "unified_languages.json"
OUTPUT = PROJECT_ROOT / "output" / "validation" / "fallback_graph.dot"

# Luo OUTPUT-kansio jos ei ole
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

def visualize_fallbacks():
    with open(UNIFIED, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    lines.append("digraph Fallbacks {")
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=box, fontname="Arial"];')

    for lang_id, info in data.items():
        fb = info.get("fallback")

        # Skip if no fallback
        if not fb:
            continue

        # Self-fallback (root languages)
        if fb == lang_id:
            lines.append(f'  "{lang_id}" [style=filled, fillcolor="#cce5ff"];')
            continue

        # Normal fallback edge
        lines.append(f'  "{lang_id}" -> "{fb}";')

    lines.append("}")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Fallback graph written to: {OUTPUT}")
    print("You can render it with:")
    print(f"dot -Tpng {OUTPUT} -o fallback_graph.png")
    print(f"dot -Tsvg {OUTPUT} -o fallback_graph.svg")


if __name__ == "__main__":
    visualize_fallbacks()

