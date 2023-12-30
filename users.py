import json

NAMES_PATH = 'assets/names/names.json'

def load_names_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
            
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} could not be decoded.")
        return []
    
def save_names_to_file(id, name):
    loaded_data = load_names_from_file(NAMES_PATH)
    new_data = {id: name}
    loaded_data.update(new_data)

    # Write the updated data back to the file
    with open(NAMES_PATH, "w") as file:
        json.dump(loaded_data, file, indent=4)


#loaded = load_names_from_file('assets/Names/names.json')
#print(len(loaded))