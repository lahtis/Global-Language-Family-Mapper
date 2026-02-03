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
from collections import Counter

SOURCE_FILE = 'master_final_indexed.json'

def show_statistics():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found. Please run master_index.py first.")
        return

    # Filter out metadata to get only actual language entries
    languages = {k: v for k, v in data.items() if k != "_metadata"}
    total_count = len(languages)

    # Collect family names for the counter
    families = [info['family_name'] for info in languages.values()]
    counter = Counter(families)

    print("\nLANGUAGE FAMILY DISTRIBUTION (Top 15)")
    print("-" * 60)
    
    # Print in descending order of frequency
    for name, count in counter.most_common(15):
        percentage = (count / total_count) * 100
        print(f"{name:<40} | {count:>5} languages ({percentage:>5.1f}%)")
    
    print("-" * 60)
    print(f"TOTAL: {total_count} languages cataloged")

if __name__ == "__main__":
    show_statistics()
