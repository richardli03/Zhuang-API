""" just adding a couple of database entries to work with the api easier"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import sys
from pathlib import Path
import json
from typing import List

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from libs.databases import Category, Exercise, Entry, Workout
from libs.db_utils import *


def add_exercises(session: Session, exercises: List[str], category_id: int):
    for exercise in exercises:
        session.add(Exercise(name=exercise, category_id=category_id))
    session.commit()


def main():
    database_name = "new_richard_workouts"
    resp = ""
    while resp.lower() not in ["y", "yes"]:
        resp = input(
            f"Are you sure you want to delete your database '{database_name}'? (y/n): "
        )
        if resp == "n":
            return

    session = create_session(database_name, True)

    # Create categories
    chest = Category(name="Chest")
    legs = Category(name="Legs")
    arms = Category(name="Arms")
    shoulders = Category(name="Shoulders")
    back = Category(name="Back")
    abs = Category(name="Abs")

    session.add(chest)
    session.add(legs)
    session.add(arms)
    session.add(shoulders)
    session.add(back)
    session.add(abs)

    # committing to the session also adds the id
    session.commit()

    with open("exercises.json", "r") as f:
        exercises = json.load(f)

    add_exercises(session, exercises["chest"], chest.id)
    add_exercises(session, exercises["arms"], chest.id)
    add_exercises(session, exercises["legs"], chest.id)
    add_exercises(session, exercises["shoulders"], chest.id)
    add_exercises(session, exercises["back"], chest.id)
    add_exercises(session, exercises["abs"], chest.id)

    # Create an entry with set info
    entry = Entry(
        time=datetime.now(),
        set_info=[
            {"weight": 150, "reps": 6},
            {"weight": 150, "reps": 6},
            {"weight": 150, "reps": 5},
            {"weight": 150, "reps": 5},
        ],
        exercise_id=1,
        workout_id=1,
    )
    entry1 = Entry(
        time=datetime.now(),
        set_info=[
            {"weight": 140, "reps": 5},
            {"weight": 140, "reps": 7},
            {"weight": 140, "reps": 7},
            {"weight": 140, "reps": 7},
        ],
        exercise_id=1,
        workout_id=1,
    )
    entry2 = Entry(
        time=datetime.now(),
        set_info=[
            {"weight": 150, "reps": 8},
            {"weight": 150, "reps": 8},
            {"weight": 150, "reps": 5},
            {"weight": 150, "reps": 5},
        ],
        exercise_id=2,
        workout_id=1,
    )
    workout = Workout(
        name="Chest Day", time=datetime.now(), entries=[entry, entry1, entry2]
    )
    # Add to session and commit
    session.add(entry)
    session.add(entry1)
    session.add(entry2)
    session.add(workout)
    session.commit()

    results = session.query(Workout).first()
    print(results)


if __name__ == "__main__":
    main()
