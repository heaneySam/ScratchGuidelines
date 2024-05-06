import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ScratchTables.settings")  # Replace 'your_project.settings' with your actual settings module
django.setup()

from tableapp.models import TrustGuideline
def delete_all_guidelines():
    # This retrieves all guidelines and deletes them
    count, _ = TrustGuideline.objects.all().delete()
    print(f"Deleted {count} guidelines from the database.")

if __name__ == "__main__":
    delete_all_guidelines()
