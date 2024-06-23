from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    exercises = relationship("Exercise", back_populates="category")

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Category: {self.name}, ID: {self.id}"


class Exercise(Base):
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
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, index=True)
    exercise_id = Column(String, ForeignKey("exercises.id"))
    set_info = Column(JSON)
    exercise = relationship("Exercise", back_populates="entries")

    def __init__(self, time, exercise_id, set_info) -> None:
        self.time = time
        self.exercise_id = exercise_id
        self.set_info = set_info

    def __repr__(self) -> str:
        return f"Entry ID: {self.id}, Exercise {self.exercise_id}: {self.exercise.name}, Time: {self.time}"
