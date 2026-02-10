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


import xml.etree.ElementTree as ET
from pathlib import Path
import json
import sys


def parse_iso639_3(path):
    iso3 = {}
    iso1 = {}
    iso2 = {}

    with open(path, "r", encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.strip()
            if not line:
                continue

            # ohita header
            if first:
                first = False
                continue

            parts = line.split("\t")

            # hyväksy 7 tai 8 saraketta
            if len(parts) < 7:
                continue

            # jos sarakkeita on enemmän, ota vain ensimmäiset 7
            parts = parts[:7]

            code3, part2b, part2t, part1, scope, ltype, name = parts

            iso3[code3] = {
                "name": name,
                "iso639_3": code3,
                "iso639_2B": part2b or "",
                "iso639_2T": part2t or "",
                "iso639_1": part1 or "",
                "scope": scope,
                "type": ltype,
            }

            if part1:
                iso1[part1] = code3

            if part2b or part2t:
                iso2[code3] = {
                    "iso639_2B": part2b or "",
                    "iso639_2T": part2t or "",
                }

    return iso1, iso2, iso3



def parse_iso639_3_names(path):
    """
    Parsii iso-639-3_Name_Index.tab:
    Id  Print_Name  Inverted_Name
    """
    names = {}

    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.strip()
            if not line:
                continue

            if first:
                first = False
                if line.startswith("Id\t"):
                    continue

            parts = line.split("\t")
            if len(parts) < 3:
                continue

            code3, print_name, inverted_name = parts

            entry = names.setdefault(code3, set())
            if print_name:
                entry.add(print_name)
            if inverted_name:
                entry.add(inverted_name)

    # muutetaan set → list
    return {k: sorted(v) for k, v in names.items()}


def parse_iso639_3_macrolanguages(path):
    """
    Parsii iso-639-3_macrolanguages.tab:
    M_Id  I_Id  I_Status
    """
    macros = {}

    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.strip()
            if not line:
                continue

            if first:
                first = False
                if line.startswith("M_Id\t"):
                    continue

            parts = line.split("\t")
            if len(parts) < 3:
                continue

            macro, individual, status = parts
            macros.setdefault(macro, []).append(individual)

    return macros


def parse_iso639_5_rdf(path):
    """
    Parsii ISO-639-5 SKOS RDF -tiedoston:
    http://id.loc.gov/vocabulary/iso639-5.skos.rdf
    """
    iso5 = {}

    path = Path(path)

    tree = ET.parse(path)
    root = tree.getroot()

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "skos": "http://www.w3.org/2004/02/skos/core#"
    }

    for concept in root.findall("rdf:Description", ns):
        about = concept.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
        if not about or "iso639-5" not in about:
            continue

        if not about.startswith("http://id.loc.gov/vocabulary/iso639-5/"):
            continue

        code = about.split("/")[-1]
        label = concept.find("skos:prefLabel", ns)

        if label is not None and label.text:
            iso5[code] = label.text

    return iso5


def parse_all_iso_files(
    iso639_3_path,
    name_index_path,
    macrolanguages_path,
    iso639_5_path,
):
    iso1, iso2, iso3 = parse_iso639_3(iso639_3_path)
    names = parse_iso639_3_names(name_index_path)
    macros = parse_iso639_3_macrolanguages(macrolanguages_path)
    iso5 = parse_iso639_5_rdf(iso639_5_path)

    return {
        "iso639_1": iso1,
        "iso639_2": iso2,
        "iso639_3": iso3,
        "iso639_3_names": names,
        "iso639_3_macrolanguages": macros,
        "iso639_5": iso5,
    }


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 4:
        print(
            "Käyttö:\n"
            "  iso_parser.py iso-639-3.tab iso-639-3_Name_Index.tab "
            "iso-639-3_macrolanguages.tab iso-639-5.skos.rdf",
            file=sys.stderr,
        )
        sys.exit(1)

    iso639_3_path, name_index_path, macrolanguages_path, iso639_5_path = argv

    data = parse_all_iso_files(
        iso639_3_path,
        name_index_path,
        macrolanguages_path,
        iso639_5_path,
    )

    # Tulostetaan JSON:ina stdoutiin
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()

