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

SOURCE_FILE = 'master_final_indexed.json'
MAP_FILE = 'conf/family_map.json'

def auto_map_v2():
    """
    Automatically maps unclassified languages based on keywords in their names.
    This helps reduce the number of 'mis' (Uncoded) entries.
    """
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            family_map = json.load(f)
    except FileNotFoundError:
        print("Error: Required files not found. Ensure the 'conf2' directory exists.")
        return

    # Mapping hints based on language name keywords
    name_hints = {
        'Sign Language': 'art',
        'Bantu': 'nic',
        'Quechua': 'qwe',
        'Arabic': 'afa',
        'Aramaic': 'afa',
        'Chinese': 'sit',
        'Sami': 'fiu',
        'Malay': 'map',
        'Island Carib': 'sai',
        'Pidgin': 'crp',
        'Creole': 'crp'
    }

    new_mappings_count = 0
    
    for bcp, info in data.items():
        # Skip the metadata block
        if bcp == "_metadata":
            continue
            
        iso_code = bcp.split('-')[0].lower()
        name = info.get('name', '')

        # Skip if already mapped to something other than 'mis' (uncoded)
        if iso_code in family_map and family_map[iso_code] != 'mis':
            continue

        found = False
        # Search for hints within the language name
        for hint, family_code in name_hints.items():
            if hint in name:
                family_map[iso_code] = family_code
                new_mappings_count += 1
                found = True
                break
        
        # Future logic for 3-letter ISO code ranges can be added here
        if not found and len(iso_code) == 3:
            pass

    # Save the updated mapping file
    try:
        with open(MAP_FILE, 'w', encoding='utf-8') as f:
            json.dump(family_map, f, indent=4, sort_keys=True)
        print(f"Auto-mapper V2 complete! Added {new_mappings_count} new language definitions.")
    except Exception as e:
        print(f"Error saving map file: {e}")

if __name__ == "__main__":
    auto_map_v2()
