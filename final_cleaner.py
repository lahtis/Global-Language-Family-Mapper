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

def check_final():
    try:
        with open('master_final_indexed.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filtteröidään: ohitetaan metadata ja etsitään "mis" (uncoded)
        # Käytetään .get(), jottei koodi kaadu jos avain puuttuu
        uncoded = {
            k: v['name'] for k, v in data.items() 
            if k != "_metadata" and isinstance(v, dict) and v.get('iso639_5') == "mis"
        }
        
        print(f"--- STATUS: {len(uncoded)} UNCODED LANGUAGES REMAINING ---")
        
        for code, name in sorted(uncoded.items())[:20]:
            print(f"{code}: {name}")
            
        if len(uncoded) > 20:
            print(f"... and {len(uncoded)-20} others.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_final()
