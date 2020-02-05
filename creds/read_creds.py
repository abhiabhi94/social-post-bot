"Read the contents of a credential file"
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_cred_file(file_loc):
    """
    Read a json file containing credentials

    Returns
        dict: The contents of the secret file in a dictionary

    Params
        file_loc: str
            The absolute or relative location with respect to this file
    """
    file_loc_abs = os.path.join(BASE_DIR, file_loc)

    with open(file_loc_abs, 'r') as json_file:
        json_file = json.load(json_file)

    return json_file
