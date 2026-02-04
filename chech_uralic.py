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

# ASETTAMALLA NÄMÄ KAKSI RIITTÄÄ
glfm_file = "GLFM_master_iso_only.json"

# OIKEA UralicNLP-KIELILISTA (42 kpl)
uralic_supported = {
    "hun","kca","mns","ekk","fin","fkv","izh","krl","zkv","liv",
    "olo","lud","fit","vep","vot","vro","mrj","mhr","myv","mdf",
    "udm","koi","kpv","sia","smn","sjk","sjd","sms","sjt","sju",
    "smj","sme","sje","sma","mtm","yrk","nio","enf","enh","rts",
    "xas","sel"
}

print("Verrataan GLFM:n uralicNLP-lippuja oikeaan UralicNLP-kielilistaan…\n")

# Lataa GLFM-master
with open(glfm_file, "r", encoding="utf-8") as f:
    glfm = json.load(f)

glfm_true = set()
glfm_false = set()

# GLFM on sanakirja, jossa avaimet ovat esim. "alu-ALU"
for key, entry in glfm.items():
    if key.startswith("_"):
        continue

    if not isinstance(entry, dict):
        continue

    iso3 = entry.get("iso639_3")
    if not iso3:
        continue

    if entry.get("uralicNLP", False):
        glfm_true.add(iso3)
    else:
        glfm_false.add(iso3)

errors = []

# 1) Kielet, joita UralicNLP tukee, mutta GLFM EI merkitse uralicNLP=True
for iso in sorted(uralic_supported):
    if iso not in glfm_true:
        errors.append(f"{iso}: UralicNLP tukee tätä, mutta GLFM EI merkitse uralicNLP=True")

# 2) Kielet, joita GLFM merkitsee uralicNLP=True, mutta UralicNLP EI tue
for iso in sorted(glfm_true):
    if iso not in uralic_supported:
        errors.append(f"{iso}: GLFM merkitsee uralicNLP=True, mutta UralicNLP EI tue tätä kieltä")

# Tulosta tulokset
if errors:
    print("❌ Löytyi eroavaisuuksia:\n")
    for e in errors:
        print(" -", e)
else:
    print("✅ GLFM ja UralicNLP vastaavat toisiaan täydellisesti!")

print(f"\nGLFM uralicNLP=True: {len(glfm_true)} kieltä")
print(f"Oikea UralicNLP-tuki: {len(uralic_supported)} kieltä")

