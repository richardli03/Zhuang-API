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
    chest_category = Category(name="Chest")

    # Create an exercise
    bench_press = Exercise(name="Bench Press", category=chest_category)

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
    )

    # Add to session and commit
    session.add(chest_category)
    session.add(bench_press)
    session.add(entry)
    session.commit()


if __name__ == "__main__":
    main()
