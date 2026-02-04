# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Global Language Family Mapper (GLFM)
# Copyright (c) 2026 Tuomas Lähteenmäki
# Licensed under the MIT License
# ------------------------------------------------------------------------
# This script is part of the GLFM project.
# See LICENSE file in the project root for full license text.
# ------------------------------------------------------------------------

import json

PATH = "GLFM_master_iso_only.json"

def main():
    with open(PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Number of languages ​​in the file: {len(data)}")

if __name__ == "__main__":
    main()

