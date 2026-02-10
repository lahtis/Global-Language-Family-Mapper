# Global Language Family Mapper (GLFM)

A modular, JSON-based language database and validation pipeline for over **7,900 languages** (ISO 639-3), including Uralic/Finno-Ugric languages. Designed for **RSS feeds, localization, and NLP workflows**.

---

## Features

- **7,900+ Languages**: Unified from ISO 639-1/2/3/5, Wiktionary, CLDR, Glottolog, and POS statistics.  
- **Accurate BCP-47 tags**: Language, script, and region combined automatically.  
- **Fallback Chains**: Automatically assigns fallback languages where applicable.  
- **Uralic/Finno-Ugric Support**: Detailed mapping for Finnish, Karelian, Estonian, and related languages.  
- **Validation Pipeline**: Full automated checks for ISO consistency, BCP-47 compliance, fallback correctness, POS stats, and Glottolog data.  
- **Graphviz Visualization**: Fallback relationships can be visualized.  

---

## Directory Structure

```json
├── build_unified.py               # Build unified JSON database
├── data/                          # Raw and processed language data
│ ├── cldr/
│ │ └── likelySubtags.json
│ ├── iso_639_*.py                 # ISO datasets in Python format
│ ├── uralic_languages.json
│ └── ...
├── loaders/                       # Data loading modules
├── logic/                         # Logic for scripts, regions, fallbacks, BCP-47
├── models/                        # Data models (Language class, ISO modules)
├── output/                        # Pipeline output
│ ├── unified/                     # unified_languages.json
│ ├── validation/                  # validation reports, errors, fallback graph
│ ├── final/
│ ├── dialects/
│ └── logs/
├── tools/                         # Validation, report generation, and helpers
├── run_full_pipeline.py           # Run full pipeline: build → validate → report
└── init.py
```

---

## Data Structure (`unified_languages.json`)

Each language is represented as a JSON object keyed by its ISO 639-3 code:

```json
"fin": {
  "id": "fin",
  "name": "Finnish",
  "official_name": "Finnish",
  "iso639_1": "fi",
  "iso639_2B": "fin",
  "iso639_2T": "fin",
  "iso639_3": "fin",
  "iso639_5": "",
  "default_script": "Latn",
  "default_region": "FI",
  "bcp47": "fi-Latn-FI",
  "fallback": "fin",
  "uralicNLP": true,
  "written": true,
  "written_scripts": ["Latn"],
  "glottocode": "finn1255",
  "family": "Uralic",
  "glottolog": {...},
  "pos_stats": {...}
}
```

- ```bcp47``` is automatically generated: ```lang[-Script][-Region]```.
- ```fallback``` is the default fallback language.
- ```uralicNLP``` is true if the language belongs to the Uralic/Finno-Ugric family.
- ```written_scripts``` lists all known writing scripts.

---

## Pipeline Overview

- The pipeline is fully automated:
- Generate ISO files (tools/generate_iso_files.py)
- Build Unified Database (build_unified.py)

---

## Validate:

- BCP-47 tags (validate_bcp47.py)
- Fallback chains (validate_fallbacks.py)
- ISO consistency (validate_iso_consistency.py)
- POS statistics (validate_pos_stats.py)
- Glottolog data (validate_glottolog.py)
- Generate Validation Reports (generate_report.py):
- Markdown report (validation_report.md)
- HTML report (validation_report.html)
- JSON error log (validation_errors.json)
- Visualize Fallback Graph (visualize_fallbacks.py)

---

## Usage

Run the full pipeline:
```python
python3 run_full_pipeline.py
```

```python
import json
from pathlib import Path

unified_file = Path("output/unified/unified_languages.json")
with unified_file.open("r", encoding="utf-8") as f:
    languages = json.load(f)

# Access Finnish
finnish = languages.get("fin")
print(finnish["bcp47"])  # fi-Latn-FI
print(finnish["uralicNLP"])  # True
```

---

## Notes
- uralic_languages.json must be present for Uralic support; pipeline will warn if missing.
- The unified database integrates ISO, Wiktionary, CLDR, Glottolog, and POS stats.
- Fallback chains ensure robust language detection for RSS feeds.

---

## License

Copyright © 2026 Tuomas Lähteenmäki

This project is licensed under the MIT License. You may use, modify, and distribute the data, provided the original copyright notice is retained.

See LICENSE for details.