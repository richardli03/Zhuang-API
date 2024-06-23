""" just adding a couple of database entries to work with the api easier"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from libs.databases import Base, Category, Exercise, Entry
from libs.db_utils import *


def main():
    session = create_session("richard_workouts", True)

    # Create a category
    chest = Category(name="Chest")
    legs = Category(name="Legs")
    arms = Category(name="Arms")
    session.add(chest)
    session.add(legs)
    session.add(arms)
    # committing to the session also adds the id
    session.commit()

    bench_press = Exercise(name="Bench Press", category_id=chest.id)
    dips = Exercise(name="Dips", category_id=chest.id)
    incline_press = Exercise(name="Incline Press", category_id=chest.id)

    # Create an entry with set info
    entry = Entry(
        time=datetime.now(),
        name=bench_press.name,
        set_info=[
            {"weight": 150, "reps": 6},
            {"weight": 150, "reps": 6},
            {"weight": 150, "reps": 5},
            {"weight": 150, "reps": 5},
        ],
        exercise_id=1,
    )
    entry1 = Entry(
        time=datetime.now(),
        name=bench_press.name,
        set_info=[
            {"weight": 140, "reps": 5},
            {"weight": 140, "reps": 7},
            {"weight": 140, "reps": 7},
            {"weight": 140, "reps": 7},
        ],
        exercise_id=1,
    )
    entry2 = Entry(
        time=datetime.now(),
        name=bench_press.name,
        set_info=[
            {"weight": 150, "reps": 8},
            {"weight": 150, "reps": 8},
            {"weight": 150, "reps": 5},
            {"weight": 150, "reps": 5},
        ],
        exercise_id=2,
    )

    # Add to session and commit

    session.add(bench_press)
    session.add(dips)
    session.add(incline_press)
    session.add(entry)
    session.add(entry1)
    session.add(entry2)
    session.commit()


if __name__ == "__main__":
    main()
