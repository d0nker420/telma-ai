import json
import uuid
from datetime import datetime

# Load JSON data from a local file
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Create a new JSON structure embedding the original JSON data
def create_new_structure(original_data):
    new_structure = {
        "id": "567e47ca-a811-4369-883a-95a560e92f1b",
        "created_at": "2024-05-09T13:49:36.558814",
        "account_id": "a3fa834d-a542-48cc-ab4e-d93a29e2c75e",
        "current_bot_version_id": "328afa66-aea1-49c1-948a-9b664607579d",
        "current_bot_version": original_data,  # Embed the original JSON data
        "labels": []
    }
    return new_structure

# Save the new JSON structure to a local file (optional)
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Pretty-print with an indent of 4 spaces

# Main function
def produce_portal_file():
    original_file_path = 'output.json'  # Replace this with the path to your original JSON file
    new_file_path = 'output-portal.json'  # Replace this with the desired path for the new JSON file

    original_data = load_json(original_file_path)  # Load original JSON data
    new_structure = create_new_structure(original_data)  # Create new JSON structure

    # Print the new structure to the console
    print(json.dumps(new_structure, indent=4))

    # Save the new JSON structure to a file
    save_json(new_file_path, new_structure)
