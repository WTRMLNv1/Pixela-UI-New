# core.py
# This script interacts with the Pixela API

import requests
from Functions.getDate import get_current_date
from Functions.getCreds import update_creds
import json
import os
PIXELA_ENDPOINT = "https://pixe.la/v1/users"

def create_user(token: str, username: str) -> dict:
    """
    Creates a new user on Pixela with the specified username and token.
    
    Args:
        token (str): The token for the Pixela user.
        username (str): The username for the Pixela user.
    Returns:
        response (dict): The response from the Pixela API after creating the user.
    """
    
    userParams = {
        "token": token,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    
    response = requests.post(PIXELA_ENDPOINT, json=userParams)
    isSuccess = response.status_code == 200 or response.status_code == 201
    if isSuccess:
        update_creds(username=username, tokenID=token)
    return response.json()

def create_graph(graph_id: str, name: str, unit: str, type: str, color: str, timezone: str, token: str, username: str) -> dict:
    """
    Creates a new graph on Pixela with the specified parameters.
    
    Args:
        graph_id (str): The ID of the graph to be created.
        name (str): The name of the graph.
        unit (str): The unit of measurement for the graph.
        type (str): The type of data the graph will hold (e.g., int, float).
        color (str): The color of the graph. Accepted values: "shibafu", "momiji", "sora", "ichou", "ajisai", or "kuro".
        timezone (str): The timezone for the graph.
        token (str): The user's token ID
        username (str): The username
    Returns:
        response (dict): The response from the Pixela API after creating the graph.
    """
    graphEndpoint = f"{PIXELA_ENDPOINT}/{username}/graphs"
    graph_params = {
        "id": graph_id,
        "name": name,
        "unit": unit,
        "type": type,
        "color": color,
        "timezone": timezone
    }

    headers = {
        "X-USER-TOKEN": token
    }

    response = requests.post(graphEndpoint, json=graph_params, headers=headers)
    isSuccess = response.status_code == 200 or response.status_code == 201
    if isSuccess:
        update_creds(graphID=graph_id, quantity=unit, quantityType=type)
    return response.json()

# Adding a pixel
def add_pixel(graph_id: str, headers: dict, quantity: str, date: str, username: str, trySend: bool = True) -> dict:
    """
    Adds a pixel to the specified graph on Pixela.
    Args:
        graph_id (str): User-generated graph id
        headers (dict): A dictionary that contains token
        quantity (str): The quantity to be added to the graph (must match graph type, e.g., "1" or "1.5")
        date (str): The date for the pixel in "YYYYMMDD" format
        username (str): The username
        trySend (bool, optional): Whether to attempt sending the request. Defaults to True.
    Returns:
        response (json): The response recieved from Pixela API
    """
    if trySend:
        pixel_params = {
            "date": date,
            "quantity": quantity
        }
        add_pixel_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graph_id}"
        response = requests.post(add_pixel_endpoint, json=pixel_params, headers=headers)
        return response.json()
    else:
        return {"message": "trySend is set to False. Pixel not added."}
CREDS_FILE = "creds.json"