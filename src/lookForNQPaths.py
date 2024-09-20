"""
This script searches for specific target strings within Ignition Perspective JSON files located in a specified directory and its subdirectories. 
It identifies the paths and parent names where the target strings are found and writes the results to a CSV file.

Functions:
- find_locations_by_string(data, target_string, path=None, parent_names=None): Recursively searches for the target string in the JSON data and returns the locations.
- find_view_json_files(folder_path): Finds all 'view.json' files in the specified directory and its subdirectories.
- main(): The main function that orchestrates the search and writes the results to a CSV file.

Usage:
1. Specify the target strings to search for in the `target_strings` list.
2. Specify the directory path to search for 'view.json' files in the `find_view_json_files` function call.
3. Run the script. The results will be written to 'results.csv' and opened automatically.
"""

import csv, json, os

def find_locations_by_string(data, target_string, path=None, parent_names=None):
    try:
        results = []

        if path is None:
            path = []

        if parent_names is None:
            parent_names = []

        # Check if the current data is a dictionary
        if isinstance(data, dict):
            # Get the 'meta/name' value if present
            meta_name = data.get('meta', {}).get('name', None)

            # If the 'meta/name' value is found, add it to the list of parent names
            if meta_name:
                parent_names.append(meta_name)

            for key, value in data.items():
                path.append(key)

                # If the target string is found in the value, add the location to the results
                if isinstance(value, str) and target_string in value:
                    parent_name = '/'.join(parent_names)  # Combine parent names for the parent name
                    key_path = '/'.join(path)  # Combine path elements for the key path
                    results.append({'targetString': target_string, 'parentName': parent_name, 'keyPath': key_path})

                results.extend(find_locations_by_string(value, target_string, path, parent_names))

                # Remove the last element from the path
                path.pop()

            # If the 'meta/name' value was added, remove it
            if meta_name:
                parent_names.pop()

        # Check if the current data is a list
        elif isinstance(data, list):
            for index, item in enumerate(data):
                path.append(str(index))

                results.extend(find_locations_by_string(item, target_string, path, parent_names))

                # Remove the last element from the path
                path.pop()

        return results
    except:
        print("Could not find")


def find_view_json_files(folder_path):
    view_json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == 'view.json':
                #print('Folder path: ' + str(os.path.join(root, file)))
                view_json_files.append(os.path.join(root, file))
    return view_json_files

def main():
    try:
        # Specify the target string you are looking for
        target_strings = ['uspGetTasklistGroupEntity',
                          'uspGetSFZoneGroupName', 
                          'uspAdhocHourAdd', 
                          'umGetCBPChartData']
  
        # Find all view.json files in the folder and subfolders
        view_json_files = find_view_json_files('C:\Program Files\Inductive Automation\Ignition\data\projects\global\com.inductiveautomation.perspective\\views')
        with open('results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Target String', 'Parent Name', 'Key Path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in target_strings:
                for file_path in view_json_files:
                    with open(file_path, 'r', encoding="utf8") as file:
                        json_data = json.load(file)

                    # Find locations with the given string and print the result
                    result = find_locations_by_string(json_data, item)
                    #print(result)
                    for entry in result:
                        parent_name = str(file_path.split('\\')[-5]) + '/' +str(file_path.split('\\')[-4]) + '/' +str(file_path.split('\\')[-3]) + '/' +  str(file_path.split('\\')[-2]) # Get the last part of the file path
                        print(f"Named Query: {entry['targetString']}, Location: {parent_name}/{entry['parentName']}, Key Path: {entry['keyPath']}")
                        writer.writerow({'Target String': entry['targetString'], 'Parent Name': f"{parent_name}/{entry['parentName']}", 'Key Path': entry['keyPath']})

        os.startfile('results.csv')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

