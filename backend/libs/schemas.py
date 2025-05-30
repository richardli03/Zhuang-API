from datetime import datetime
from pydantic import BaseModel
from typing import Union, List


class CategoryInput(BaseModel):
    name: str


class CategoryOutput(BaseModel):
    id: int
    name: str


class ExerciseInput(BaseModel):
    name: str
    category_id: int


class ExerciseOutput(BaseModel):
    id: int
    name: str
    category_id: int


class EntryInput(BaseModel):
    name: str
    set_info: List[dict]
    workout_id: int


class EntryOutput(BaseModel):
    id: int
    time: datetime
    set_info: List[dict]
    exercise_id: int
    workout_id: int


class WorkoutOutput(BaseModel):
    id: int
    name: str
    time: datetime
    entries: List[EntryOutput]


class WorkoutInput(BaseModel):
    name: str
