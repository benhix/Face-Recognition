import json

def load_names_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('names', [])
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} could not be decoded.")
        return []