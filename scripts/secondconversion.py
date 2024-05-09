import os
import json
import shutil


def clean_filename(filename):
    # Removes unwanted characters and returns a clean version
    return filename.replace('_', ' ').replace('-', ' ')


def title_case_filename(filename):
    # Converts filename to title case
    return ' '.join(word.capitalize() for word in filename.split())


def create_json_object(subdir, filename, new_filename):
    parts = subdir.split()
    medical_speciality = ' '.join(parts[:-1])
    locality = parts[-1]
    original_filename = subdir.replace(' ', '-') + '-' + filename
    external_url = f"https://uhdlocalguidelines.s3.amazonaws.com/{original_filename.replace(' ', '-')}"

    return {
        "original_filename": original_filename,
        "name": clean_filename(filename.rsplit('.', 1)[0]),
        "medical_speciality": medical_speciality,
        "locality": locality,
        "external_url": external_url,
        "trust": "UHD"
    }


def process_directory(root_dir):
    data = []
    new_folder = os.path.join(root_dir, "Renamed Files")
    os.makedirs(new_folder, exist_ok=True)

    for subdir, dirs, files in os.walk(root_dir):
        if dirs:
            continue  # Skip processing at higher directory levels
        rel_dir = os.path.relpath(subdir, root_dir)
        for filename in files:
            new_filename = f"{rel_dir.replace(' ', '-')}-{filename}".replace(' ', '-').title()
            json_object = create_json_object(rel_dir, filename, new_filename)
            data.append(json_object)

            # Copy and rename file
            original_path = os.path.join(subdir, filename)
            new_path = os.path.join(new_folder, new_filename)
            shutil.copy2(original_path, new_path)

    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)


# Replace 'root_directory_path' with the path to the directory you want to process
root_directory_path = 'upload2'
process_directory(root_directory_path)
