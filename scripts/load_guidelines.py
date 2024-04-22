import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ScratchTables.settings")
django.setup()

from tableapp.models import TrustGuideline, Trust


def load_data():
    # Path to your JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'Guidelines_Example_Data.json')

    # Load data from JSON
    with open(file_path, 'r') as file:
        guidelines = json.load(file)

    # Assuming you have a default trust or you'll need to create/select a trust
    default_trust, _ = Trust.objects.get_or_create(name="RCEM Website")

    for guideline in guidelines:
        TrustGuideline.objects.create(
            trust=default_trust,
            name=guideline['name'],
            description=guideline['description'],
            external_url=guideline['url'],
            medical_speciality=guideline['medical_speciality']
        )

    print("Data loaded successfully.")


if __name__ == "__main__":
    load_data()
