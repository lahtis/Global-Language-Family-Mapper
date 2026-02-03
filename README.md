# Global Language Family Mapper (GLFM)

A comprehensive JSON database that maps over 7,700 languages (ISO 639-3) to their respective language families (ISO 639-5). This library was specifically developed for language validation in RSS tools and localization workflows.

## Features

* **7,782 Languages**: Extracted and indexed from global linguistic datasets.
* **90% Genealogical Coverage**: 0% missing entries. All languages are classified, with ~10% grouped under uncoded or isolated categories pending further refinement.
* **Enhanced Uralic Support**: Detailed mapping for Finno-Ugric languages, including Karelian (`krl-KRL`), Finnish, and Estonian.
* **Global Geographic Accuracy**: Languages are grouped into major families such as Indo-European, Niger-Kordofanian, Austronesian, and more.

## Data Structure

- `master_final_indexed.json`: The primary index containing language names, BCP47 codes, and language family metadata.
- `conf/family_map.json`: A lookup table mapping ISO codes to family codes.
- `conf/family_names.json`: Human-readable names for the family codes used.
- `conf/iso_map.json`:
- `conf/spoken_languages.json`:

## Usage

The data is provided in standard JSON format, making it compatible with any programming language.

### Python Example:
```python
import json

# Example: Fetching details for the Karelian language
with open('master_final_indexed.json', 'r', encoding='utf-8') as f:
    languages = json.load(f)
    karelian = languages.get('krl-KRL')
    print(karelian)
    
```  
## Notice
“This project aggregates and normalizes data from multiple open linguistic sources. See SOURCES.md for details.”

## License
Copyright © 2026 Tuomas Lähteenmäki
This project is licensed under the MIT License. You are free to use, modify, and distribute the data, provided that the original copyright notice is retained.    

Licensed under the MIT License. See LICENSE for details.