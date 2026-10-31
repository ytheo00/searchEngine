import os
import json
import re


def main():
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)
        sorted_dict = dict(sorted(inverted_index.items()))
        
    alphanumeric_dicts = {}
    special_chars_dict = {}
    for key, value in sorted_dict.items():
        first_char = key[0]
        if re.match(r'^[a-zA-Z0-9]$', first_char):
            if first_char not in alphanumeric_dicts:
                alphanumeric_dicts[first_char] = {}
            alphanumeric_dicts[first_char][key] = value
        else:
            special_chars_dict[key] = value
    # Create a folder to store the JSON files
    folder_name = 'dictionary_files'
    os.makedirs(folder_name, exist_ok=True)

    # Write JSON files for alphanumeric characters
    for char, sub_dict in alphanumeric_dicts.items():
        filename = os.path.join(folder_name, f"{char}_dictionary.json")
        with open(filename, 'w') as json_file:
            json.dump(sub_dict, json_file)
        print(f"Dictionary for '{char}' written to {filename}")

    # Write JSON file for special characters
    if special_chars_dict:
        filename = os.path.join(folder_name, "special_characters_dictionary.json")
        with open(filename, 'w') as json_file:
            json.dump(special_chars_dict, json_file)
        print(f"Dictionary for special characters written to {filename}")
    
if __name__ == "__main__":
    main()