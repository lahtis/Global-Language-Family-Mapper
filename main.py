# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Global Language Family Mapper (GLFM) - Main Entry Point
# Copyright (c) 2026 Tuomas Lähteenmäki
# Licensed under the MIT License
# ------------------------------------------------------------------------

import subprocess
import sys

def run_script(script_name):
    """Utility to run a python script and wait for it to finish."""
    print(f"--- Running {script_name} ---")
    try:
        # Ajaa skriptin käyttäen samaa python-tulkkia kuin main.py
        subprocess.run([sys.executable, script_name], check=True)
        print(f"--- {script_name} finished successfully ---\n")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_name} failed. Execution stopped.")
        sys.exit(1)

def main():
    print("================================================")
    print("   GLFM: GLOBAL LANGUAGE FAMILY MAPPER          ")
    print("   Project GLFM | 2026 Tuomas Lähteenmäki    ")
    print("================================================\n")

    # 1. PUHDISTUS: Luodaan täydellinen kielikartta ilman aukkoja
    run_script("super_mapper.py")

    # 2. RAKENTAMINEN: Luodaan lopullinen JSON ja käännetään nimet
    run_script("auto_mapper.py")

    # 3. ANALYYSI: Tulostetaan tilastot ja tarkistetaan laatu
    run_script("family_stats.py")
    run_script("check_final.py")

    print("================================================")
    print("   PIPELINE COMPLETE: Your database is ready!   ")
    print("================================================")

if __name__ == "__main__":
    main()
