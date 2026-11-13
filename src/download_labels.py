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
    "active_ingredient",
    "indications_and_usage",
    "dosage_and_administration",
    "dosage_forms_and_strengths",
    "boxed_warning",
    "warnings",
    "warnings_and_cautions",
    "do_not_use",
    "ask_doctor",
    "stop_use",
    "contraindications",
    "drug_interactions",
    "adverse_reactions",
    "use_in_specific_populations",
    "pregnancy",
    "pediatric_use",
    "overdosage",
]

LABELS_PER_DRUG = 5

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for drug in DRUGS:
    url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f'openfda.generic_name:"{drug}"',
        "limit": LABELS_PER_DRUG,
    }
    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        print(f"Could not get {drug} (status {response.status_code})")
        continue

    labels = []
    for label in response.json()["results"]:
        entry = {
            "set_id": label.get("set_id"),
            "brand_names": label.get("openfda", {}).get("brand_name", []),
        }
        for section in SECTIONS:
            if section in label:
                entry[section] = label[section]
        labels.append(entry)

    with open(OUTPUT_DIR / f"{drug}.json", "w") as f:
        json.dump({"drug": drug, "labels": labels}, f, indent=2)

    print(f"Saved {drug}: {len(labels)} labels")
    time.sleep(1)