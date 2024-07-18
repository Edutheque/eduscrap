import requests
from bs4 import BeautifulSoup
import json

# URL of the website
url = "https://www.education.gouv.fr/les-programmes-du-college-3203"

# Send a GET request to the website
response = requests.get(url)

# Parse the content of the response
soup = BeautifulSoup(response.content, 'html.parser')


# Function to extract the programs
def extract_programs(content: BeautifulSoup):
    programs = []

    # Find all <h2> elements with class "title" for the levels
    levels = content.find_all('h2', class_='title')
    for level in levels:
        level_name = level.text.strip()
        level_data = {'level': level_name, 'subjects': []}

        # Find all following <h3> elements with class "title" for the subjects
        subjects = level.find_all_next('h3', class_='title')
        for subject in subjects:
            # Stop if we reach the next level or a different unrelated section
            if subject.find_previous('h2', class_='title') != level:
                break
            subject_name = subject.text.strip()
            subject_data = {'subject': subject_name, 'content': []}

            # Collect the content related to each subject
            for sibling in subject.find_next_siblings():
                if sibling.name == 'h3' or (sibling.name == 'h2' and sibling != level):
                    break
                if sibling.name in ['p', 'ul']:
                    subject_data['content'].append(sibling.text.strip())

            level_data['subjects'].append(subject_data)
        programs.append(level_data)

    return programs


# Extract the programs
programs = extract_programs(soup)

# Save the results to a JSON file
with open('programs.json', 'w', encoding='utf-8') as f:
    json.dump(programs, f, ensure_ascii=False, indent=4)

print("Programs have been successfully extracted and saved to programs.json")
