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

def list_uncoded():
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter uncoded languages, skipping the metadata block
        uncoded = [
            f"{k}: {v['name']}" for k, v in data.items() 
            if k != "_metadata" and (
                v.get('iso639_5') == "mis" or 
                "Uncoded" in v.get('family_name', '')
            )
        ]
        
        print(f"--- FOUND {len(uncoded)} UNCODED LANGUAGES ---")
        
        for item in uncoded[:20]:  # Show first 20
            print(item)
            
        if len(uncoded) > 20:
            print(f"... and {len(uncoded)-20} more.")
            
        if len(uncoded) == 0:
            print("Cleanup successful: No uncoded languages remaining.")
            
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found.")

if __name__ == "__main__":
    list_uncoded()
