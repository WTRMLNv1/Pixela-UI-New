# getCreds.py
# This script retrieves the Pixela API credentials from a file.

import json
from pathlib import Path

def get_creds(file_name : str = "creds.json") -> dict:
    """
    Retrieves Pixela API credentials from a JSON file.
    Args:
        file_name (str): (optional) The name of the JSON file containing the credentials. Default set to "creds.json" - the original file in the folder.
    Returns:
        dict: A dictionary containing the Pixela API credentials.
    """
    basePath = Path(__file__).parent.parent
    file_path = basePath /"json"/file_name
    try:
        with open(file_path, 'r') as file:
            creds = json.load(file)
            return creds
    except FileNotFoundError:
        return {"error": "Credentials file not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON from credentials file."}

def update_creds(username=None, tokenID=None, graphID=None, quantity=None, quantityType=None, lastGraphID=None, accent_color=None) -> None: 
    """
        Updates the creds.json file with new values for any provided fields.
        Existing values are preserved if not explicitly updated.
        Args:
            username (str): the username to update. Set to None
            tokenID (str): the user-generated token ID.  Set to None
            graphID (str): graph ID for the graph. Set to None
            quantity (str): The unit to use in the graph Set to None
            quantityType (str): The type of unit to use in the graph (accepted values: int or float). Set to None
            lastGraphID (str): The last used graph ID. Set to None
            accent_color (str): The accent color in hex format. Set to None
    """
    basePath = Path(__file__).parent.parent
    file_path = basePath /"json"/"creds.json"
    # Load existing creds (or use defaults if file doesn't exist)
    if file_path.exists():
        with open(file_path, "r") as file:
            creds = json.load(file)
    else:
        creds = {
            "username": None,
            "tokenID": None,
            "graphID": None,
            "quantity": None,
            "quantityType": None
        }

    # Update only the provided fields
    if username is not None:
        creds["username"] = username
    if tokenID is not None:
        creds["tokenID"] = tokenID
    # If both username and token are changed together, clear other graph-specific fields
    if (username is not None) and (tokenID is not None):
        creds["graphID"] = []
        creds["quantity"] = []
        creds["quantityType"] = []
        creds["lastGraphID"] = None
    if graphID is not None:
        creds["graphID"].append(graphID)
    if quantity is not None:
        creds["quantity"].append(quantity)
    if quantityType is not None:
        creds["quantityType"].append(quantityType)
    if lastGraphID is not None:
        creds["lastGraphID"] = lastGraphID
    if accent_color is not None:
        creds["accent_color"] = accent_color
    # Save the updated creds
    with open(file_path, "w") as file:
        json.dump(creds, file, indent=4)
