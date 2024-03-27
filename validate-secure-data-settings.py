import argparse
import json
import os
import sys

# Add a global variable to track if any items are not present
items_not_present = False

def find_nodes_in_dict(dict_obj, type_string):
    """
    Recursively searches for actions in a dictionary object and checks if they have secure data properties.

    Args:
        dict_obj (dict): The dictionary object to search in.
        type_string (str): The type of Logic App entity (actions or triggers) to search for.

    Returns:
        None
    """
    global items_not_present

    if type_string in dict_obj:
        for action_name, action_value in dict_obj[type_string].items():
            print(f"Name: {action_name}")
            if 'runtimeConfiguration' in action_value and 'secureData' in action_value['runtimeConfiguration']:
                print("\t'runtimeConfiguration' node with 'secureData' child is present")
                if 'properties' in action_value['runtimeConfiguration']['secureData']:
                    properties = action_value['runtimeConfiguration']['secureData']['properties']

                    if 'inputs' in properties:
                        print("\t\t'inputs' is present in 'properties'")
                    else:
                        print("\033[91m\t\t'inputs' is not present in 'properties'\033[0m")
                        items_not_present = True

                    if 'outputs' in properties:
                        print("\t\t'outputs' is present in 'properties'")
                    else:
                        print("\033[91m\t\t'outputs' is not present in 'properties'\033[0m")
                        items_not_present = True
                else:
                    print("\033[91m\t\t'properties' is not present in 'secureData'\033[0m")
            else:
                print("\033[91m\t'runtimeConfiguration' node with 'secureData' child is not present\033[0m")
                items_not_present = True

    for _, value in dict_obj.items():
        if isinstance(value, dict):
            find_nodes_in_dict(value, type_string)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    find_nodes_in_dict(item, type_string)

# Create the parser
parser = argparse.ArgumentParser(description='Process a directory for JSON files.')
parser.add_argument('DirPath', metavar='dirpath', type=str, help='the path to the directory')
parser.add_argument('--exit-code', action='store_true', help='return a non-zero exit code if any items are not present')

# Execute the parse_args() method
args = parser.parse_args()

# Walk the directory structure
for dirpath, dirnames, filenames in os.walk(args.DirPath):
    for filename in filenames:
        if filename == 'workflow.json':
            filepath = os.path.join(dirpath, filename)
            with open(filepath) as f:
                data = json.load(f)
            print(f"\nProcessing file: {filepath}")
            print("\nActions\n=======")
            find_nodes_in_dict(data, 'actions')
            print("\nTriggers\n========")
            find_nodes_in_dict(data, 'triggers')

if items_not_present and args.exit_code:
    sys.exit(1)