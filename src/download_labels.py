import json
import time
from pathlib import Path

import requests

DRUGS = [
    "ibuprofen", "acetaminophen", "metformin", "lisinopril",
    "atorvastatin", "amoxicillin", "omeprazole", "sertraline",
    "amlodipine", "levothyroxine",
]

SECTIONS = [
    "indications_and_usage",
    "dosage_and_administration",
    "warnings",
    "boxed_warning",
    "contraindications",
    "drug_interactions",
    "adverse_reactions",
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for drug in DRUGS:
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f'openfda.generic_name:"{drug}"', "limit": 1}
    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        print(f"Could not get {drug} (status {response.status_code})")
        continue

    label = response.json()["results"][0]
    cleaned = {"drug": drug}
    for section in SECTIONS:
        cleaned[section] = label.get(section, [])

    with open(OUTPUT_DIR / f"{drug}.json", "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"Saved {drug}")
    time.sleep(1)