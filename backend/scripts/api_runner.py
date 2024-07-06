import requests
import json
from pprint import pprint
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from libs.schemas import EntryInput

URL = "http://127.0.0.1:8000"


def get_categories():
    response = requests.get(f"{URL}/categories/")
    return response.json()


def get_exercises():
    response = requests.get(f"{URL}/exercises/")
    return response.json()


def get_entries():
    response = requests.get(f"{URL}/entries/")
    return response.json()


def create_category(category_name: str):
    """Remember, `params` are useful for when the input to your
    request is simple enough to be included in the URL

    Args:
        category_name (str): _description_

    Returns:
        _type_: _description_
    """
    response = requests.post(
        f"{URL}/categories/",
        params={"category_name": category_name},
        headers={"accept": "application/json"},
    )
    return response


def create_exercise(exercise_name: str, exercise_category: int):
    entry = {"name": exercise_name, "category_id": exercise_category}
    response = requests.post(
        f"{URL}/exercises/",
        json=entry,
        headers={"Content-Type": "application/json", "accept": "application/json"},
    )
    return response


def create_entry(entry_name, set_info: list[dict]):
    entry = {"name": entry_name, "set_info": set_info}
    response = requests.post(
        f"{URL}/entries/",
        headers={"Content-Type": "application/json", "accept": "application/json"},
        json=entry,
    )
    return response.json()


set_info = [
    {"weight": 30, "reps": 12},
    {"weight": 30, "reps": 12},
    {"weight": 30, "reps": 12},
]

entry_name = "Bench Press"

create_entry(entry_name, set_info)
create_exercise("another test", 2)
# create_a_category("Test3")


pprint(get_exercises())
