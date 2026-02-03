# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Global Language Family Mapper (GLFM)
# Copyright (c) 2026 Tuomas Lähteenmäki
# Licensed under the MIT License
# ------------------------------------------------------------------------
# This script is part of the krl-KRL project.
# See LICENSE file in the project root for full license text.
# ------------------------------------------------------------------------

import json

# Configuration and file paths
SOURCE_FILE = 'conf/spoken_languages.json'
TARGET_FILE = 'master_final_indexed.json'
MAP_FILE = 'conf/family_map.json'
NAME_FILE = 'conf/family_names.json'
ISO_MAP_FILE = 'conf/iso_map.json'

def run_enrichment():
    """
    Enriches the base language list with family data and ISO mappings.
    """
    try:
        # Load all configuration mapping files
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            lang_to_family = json.load(f)
        with open(NAME_FILE, 'r', encoding='utf-8') as f:
            family_names = json.load(f)
        with open(ISO_MAP_FILE, 'r', encoding='utf-8') as f:
            iso_map = json.load(f)
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            languages_list = json.load(f)
    except Exception as e:
        print(f"Error loading configuration files: {e}")
        return

    # Initialize output dictionary with project metadata
    final_data = {
        "_metadata": {
            "copyright": "Copyright (c) 2026 Tuomas Lähteenmäki",
            "license": "MIT",
            "description": "Global Language Family Mapper database",
            "source": "GLFM project"
        }
    }

    for lang in languages_list:
        bcp = lang.get('bcp47') or lang.get('code', '')
        if not bcp:
            continue
            
        iso3 = bcp.split('-')[0].lower()
        
        # Lookup family code, name, and ISO-639-1 code from loaded mappings
        family_code = lang_to_family.get(iso3, "mis")
        family_name = family_names.get(family_code, "Uncoded/Isolated languages")
        iso1 = iso_map.get(iso3, "")
        is_uralic = (family_code == "fiu")

        # Map the enriched data
        final_data[bcp] = {
            "name": lang.get('name', ''),
            "family_name": family_name,
            "official_name": lang.get('name', ''),
            "iso639_5": family_code,
            "iso639_3": iso3,
            "iso639_2": iso3,
            "iso639_1": iso1,
            "bcp47": bcp,
            "fallback": bcp,
            "uralicNLP": is_uralic,
            "type": "Speech"
        }

    # Save the final enriched database to the target file
    try:
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        print(f"--- ENRICHMENT COMPLETE ({TARGET_FILE} updated) ---")
    except Exception as e:
        print(f"Error saving the final file: {e}")

if __name__ == "__main__":
    run_enrichment()
