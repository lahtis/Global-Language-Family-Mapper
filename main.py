# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Global Language Family Mapper (GLFM)
# Copyright (c) 2026 Tuomas Lähteenmäki
# Licensed under the MIT License
# ------------------------------------------------------------------------
# This script is part of the GLFM project.
# See LICENSE file in the project root for full license text.
# ------------------------------------------------------------------------

import subprocess
import sys

def run_script(script_name):
    """Utility to run a python script and wait for it to finish."""
    print(f"--- Running {script_name} ---")
    try:        
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

    # 1. BUILD: Generate final JSON and translate names
    run_script("build_glfm_master.py")

    # 2. URALIC language code check
    run_script("chech_uralic.py")

    # 3. ANALYSIS: Print statistics and check quality
    
    run_script("count_languages.py")
    run_script("check_final.py")

    print("================================================")
    print("   PIPELINE COMPLETE: Your database is ready!   ")
    print("================================================")

if __name__ == "__main__":
    main()
