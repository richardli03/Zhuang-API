from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Category(Base):
    """Each category references a body part to which exercises belong.
    For example, Chest, Legs, Arms, etc."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    exercises = relationship("Exercise", back_populates="category")

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Category: {self.name}, ID: {self.id}"


class Exercise(Base):
    """Each exercise belongs to a category and has a name
    (ex: shoulder press belongs to shoulders)


    NOTE: Entries are associated with exercises with a weight and rep/set count.
    (ex: 3 sets of 10 reps of shoulder press at 50 lbs)
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="exercises")
    entries = relationship("Entry", back_populates="exercise")

    def __init__(self, name, category_id) -> None:
        self.name = name
        self.category_id = category_id

    def __repr__(self) -> str:
        return f"Exercise: {self.name}, ID: {self.id}"


class Entry(Base):
    """The "unit" of Zhuang, an entry is a single instance of an exercise
    with a set of weights and reps formatted as a list of dictionaries.
    """

    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, index=True)
    exercise_id = Column(String, ForeignKey("exercises.id"))
    set_info = Column(JSON)
    exercise = relationship("Exercise", back_populates="entries")

    # allow an entry to be associated with a workout
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    workout = relationship("Workout", back_populates="entries")

    def __init__(self, time, exercise_id, workout_id, set_info) -> None:
        self.time = time
        self.exercise_id = exercise_id
        self.workout_id = workout_id
        self.set_info = set_info

    def __repr__(self) -> str:
        return f"Entry ID: {self.id}, Exercise {self.exercise_id}: {self.exercise.name}, Time: {self.time}"


class Workout(Base):
    """A workout is how the user will interact with the databases
    A workout is a list of entries.
    """

    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, index=True)
    name = Column(String, nullable=True)  # should probably eventually set up templates
    entries = relationship("Entry", back_populates="workout")

    def __init__(self, name, time, entries) -> None:
        self.name = name
        self.time = time
        self.entries = entries

    def __repr__(self):
        return f"Workout: {self.id}, {self.entries}"
