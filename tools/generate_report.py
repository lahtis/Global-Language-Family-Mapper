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
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import html

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS = PROJECT_ROOT / "tools"
OUTPUT_ROOT = PROJECT_ROOT / "output" / "validation"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

UNIFIED = PROJECT_ROOT / "output" / "unified" / "unified_languages.json"
VALIDATION_ERRORS_JSON = OUTPUT_ROOT / "validation_errors.json"

# Validointiskriptit
VALIDATE_BCP47 = TOOLS / "validate_bcp47.py"
VALIDATE_FALLBACKS = TOOLS / "validate_fallbacks.py"
VALIDATE_ISO = TOOLS / "validate_iso_consistency.py"


def run_validation(script: Path):
    """Ajaa validointiskriptin ja palauttaa stdout + stderr."""
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()


def generate_report():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # --- Aja validoinnit ---
    bcp47_out, bcp47_err = run_validation(VALIDATE_BCP47)
    fb_out, fb_err = run_validation(VALIDATE_FALLBACKS)
    iso_out, iso_err = run_validation(VALIDATE_ISO)

    # --- Tallenna virheet JSON:iin ---
    errors_json = {
        "bcp47": bcp47_out.splitlines() if bcp47_out and "OK" not in bcp47_out else [],
        "bcp47_stderr": bcp47_err.splitlines() if bcp47_err else [],
        "fallbacks": fb_out.splitlines() if fb_out and "All fallback chains are valid" not in fb_out else [],
        "fallbacks_stderr": fb_err.splitlines() if fb_err else [],
        "iso": iso_out.splitlines() if iso_out and "All ISO codes are valid" not in iso_out else [],
        "iso_stderr": iso_err.splitlines() if iso_err else [],
    }

    with open(VALIDATION_ERRORS_JSON, "w", encoding="utf-8") as f:
        json.dump(errors_json, f, ensure_ascii=False, indent=2)

    # --- Lataa unified ---
    with open(UNIFIED, "r", encoding="utf-8") as f:
        unified = json.load(f)
    lang_count = len(unified)

    # --- Markdown-raportti ---
    md = f"""# Unified Pipeline Report
**Generated:** {timestamp}

## Summary
- Total languages: **{lang_count}**
- BCP‑47 validation: {"OK" if not errors_json['bcp47'] else "Errors found"}
- Fallback validation: {"OK" if not errors_json['fallbacks'] else "Errors found"}
- ISO validation: {"OK" if not errors_json['iso'] else "Errors found"}

---

## BCP‑47 Validation Output
{bcp47_out or "No output"}
{bcp47_err or ""}

## Fallback Validation Output
{fb_out or "No output"}
{fb_err or ""}

## ISO Validation Output
{iso_out or "No output"}
{iso_err or ""}

---
"""
    md_path = OUTPUT_ROOT / "validation_report.md"
    md_path.write_text(md, encoding="utf-8")

    # --- HTML-raportti ---
    def render_error_table(title, error_list):
        if not error_list:
            return f"<h3>{title}</h3><p>No errors.</p>"
        rows = "".join(f"<tr><td>{html.escape(e)}</td></tr>" for e in error_list)
        return f"""
<h3>{title}</h3>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>Error</th></tr>
{rows}
</table>
"""

    errors_html = ""
    errors_html += render_error_table("BCP-47 Errors", errors_json.get("bcp47", []))
    errors_html += render_error_table("Fallback Errors", errors_json.get("fallbacks", []))
    errors_html += render_error_table("ISO Errors", errors_json.get("iso", []))

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Unified Pipeline Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}
pre {{
    background: #f0f0f0;
    padding: 10px;
    border-radius: 6px;
    white-space: pre-wrap;
}}
.ok {{ color: green; font-weight: bold; }}
.err {{ color: red; font-weight: bold; }}
table {{ border-collapse: collapse; margin-bottom: 20px; }}
th, td {{ border: 1px solid #ccc; padding: 5px; }}
</style>
</head>
<body>

<h1>Unified Pipeline Report</h1>
<p><strong>Generated:</strong> {timestamp}</p>

<h2>Summary</h2>
<ul>
  <li>Total languages: <strong>{lang_count}</strong></li>
  <li>BCP‑47 validation: <span class="{'ok' if not errors_json['bcp47'] else 'err'}">{'OK' if not errors_json['bcp47'] else 'Errors found'}</span></li>
  <li>Fallback validation: <span class="{'ok' if not errors_json['fallbacks'] else 'err'}">{'OK' if not errors_json['fallbacks'] else 'Errors found'}</span></li>
  <li>ISO validation: <span class="{'ok' if not errors_json['iso'] else 'err'}">{'OK' if not errors_json['iso'] else 'Errors found'}</span></li>
</ul>

<h2>BCP‑47 Validation Output</h2>
<pre>{html.escape(bcp47_out or "No output")}{("\n" + html.escape(bcp47_err)) if bcp47_err else ""}</pre>

<h2>Fallback Validation Output</h2>
<pre>{html.escape(fb_out or "No output")}{("\n" + html.escape(fb_err)) if fb_err else ""}</pre>

<h2>ISO Validation Output</h2>
<pre>{html.escape(iso_out or "No output")}{("\n" + html.escape(iso_err)) if iso_err else ""}</pre>

<h2>Detailed Validation Errors</h2>
{errors_html}

</body>
</html>
"""

    html_path = OUTPUT_ROOT / "validation_report.html"
    html_path.write_text(html_content, encoding="utf-8")

    print(f"Markdown report written to: {md_path}")
    print(f"HTML report written to: {html_path}")
    print(f"Validation errors JSON written to: {VALIDATION_ERRORS_JSON}")


if __name__ == "__main__":
    generate_report()

