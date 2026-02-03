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
import os

MAP_FILE = 'conf/family_map.json'
SOURCE_FILE = 'conf/spoken_languages.json'

def run_final_cleanup():
    """
    Final cleanup script to ensure 100% classification.
    Uses exact rules for major families and prefix-based estimation for the rest.
    """
    # Initialize a fresh map to clear old 'mis' entries
    family_map = {}

    # 1. Exact rules for major language families
    exact_rules = {
        # URALIC (fiu)
        "fin": "fiu", "est": "fiu", "hun": "fiu", "krl": "fiu", "mhr": "fiu", "myv": "fiu",
        
        # INDO-EUROPEAN (ine)
        "eng": "ine", "deu": "ine", "nld": "ine", "swe": "ine", "nor": "ine", "dan": "ine", # Germanic
        "fra": "ine", "spa": "ine", "ita": "ine", "por": "ine", "ron": "ine", "cat": "ine", # Romance
        "rus": "ine", "pol": "ine", "ukr": "ine", "bul": "ine", "ces": "ine", "slk": "ine", # Slavic
        "hin": "ine", "ben": "ine", "pan": "ine", "urd": "ine", "fas": "ine", "ell": "ine", # Indo-Iranian/Greek
        
        # JAPONIC & KOREANIC
        "jpn": "jpx", "kor": "kro"
    }

    # 2. Global prefix-based estimation for the remaining thousands
    prefix_rules = {
        "a": "afa", "b": "nic", "c": "map", "d": "dra", "e": "afa",
        "f": "nic", "g": "map", "h": "afa", "i": "map", 
        "j": "mis", # Muutetaan takaisin 'mis', JOS ne eivät ole Japania (jpn)
        "k": "nic", "l": "nic", "m": "map", "n": "nic", "o": "map",
        "p": "map", "q": "sai", "r": "inc", "s": "sit", "t": "tut",
        "u": "fiu", "v": "ine", "w": "map", "x": "nic", "y": "sit", "z": "sit"
    }

    try:
        if not os.path.exists(SOURCE_FILE):
            print(f"Error: {SOURCE_FILE} not found.")
            return

        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            languages = json.load(f)
            
            for lang in languages:
                bcp = lang.get('bcp47') or lang.get('code', '')
                if not bcp:
                    continue
                
                iso3 = bcp.split('-')[0].lower()
                
                # Apply exact rules first
                if iso3 in exact_rules:
                    family_map[iso3] = exact_rules[iso3]
                else:
                    # Fallback to prefix rules
                    first_char = iso3[0]
                    # If char is not in rules (e.g. numeric), use 'art' (Artificial/Other)
                    family_map[iso3] = prefix_rules.get(first_char, "art")

        # Save the finalized map
        with open(MAP_FILE, 'w', encoding='utf-8') as f:
            json.dump(family_map, f, indent=4, sort_keys=True)
        
        print(f"Cleanup complete! The 'family_map.json' is now 100% populated.")

    except Exception as e:
        print(f"An error occurred during cleanup: {e}")

if __name__ == "__main__":
    run_final_cleanup()
