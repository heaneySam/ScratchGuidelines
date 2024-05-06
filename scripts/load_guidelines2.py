import re
import json


def extract_guidelines_from_file(file_path):
    # Read text data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()

    # Regex to find medical specialty and associated URLs
    pattern = r"^\s{4}(\w[\w\s]+)\n((?:\s+- https:\/\/[^\n]+\n)+)"
    matches = re.finditer(pattern, text_data, re.MULTILINE)

    # Dictionary to store the results
    guidelines = []

    # Process each match
    for match in matches:
        medical_speciality = match.group(1).strip()
        urls = match.group(2).strip().splitlines()

        for url in urls:
            url = url.strip().split(' - ')[-1]
            guideline_name = re.sub(r'https?://[^/]+/|\.[a-zA-Z0-9]+$|[\s\-_]+', ' ', url).title().strip()
            # Remove unnecessary parts to clean up the name, might need adjustment based on actual titles
            guideline_name = re.sub(r'Policies|Pdf|Pd|Docx', '', guideline_name).strip()

            guidelines.append({
                "name": guideline_name,
                "url": url,
                "description": guideline_name,  # Assuming the description can be the same as the name
                "medical_speciality": medical_speciality
            })

    # Output the data in JSON format
    return json.dumps(guidelines, indent=4)

print("in here")
# Use the function to extract guidelines from the specified text file
output_json = extract_guidelines_from_file('guidelines_text.txt')
print(output_json)
