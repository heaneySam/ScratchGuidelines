import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ScratchTables.settings")
django.setup()

from tableapp.models import TrustGuideline, Trust


def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'All_UHD_Policies.json')
    with open(file_path, 'r') as file:
        guidelines = json.load(file)

    default_trust, _ = Trust.objects.get_or_create(name="UHD")

    for guideline in guidelines:
        obj, created = TrustGuideline.objects.get_or_create(
            trust=default_trust,
            name=guideline['Title'],
            defaults={
                'description': guideline['Description'],
                'external_url': guideline['URL'],
                'medical_speciality': guideline['Medical Specialty']
            }
        )
        if created:
            print(f"Added new guideline: {guideline['Title']}")
        else:
            print(f"Skipped duplicate guideline: {guideline['Title']}")

    print("Data loading process completed.")

if __name__ == "__main__":
    load_data()
