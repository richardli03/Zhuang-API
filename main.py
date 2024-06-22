from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import uvicorn
from libs.db_utils import create_session
from typing import Union, List
from pydantic import BaseModel
from datetime import datetime
from libs.databases import Category, Exercise, Entry

app = FastAPI()


class CategoryModel(BaseModel):
    id: int
    name: str


class ExerciseModel(BaseModel):
    id: int
    name: str
    category_id: int


class EntryModel(BaseModel):
    id: int
    time: datetime
    name: str
    set_info: List[dict]
    exercise_id: int


def get_db():
    session = create_session("richard_workouts")
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def read_root():
    return "workout tracker"


@app.post("/categories/", response_model=str)
def create_category(category_name: str, db: Session = Depends(get_db)):
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/categories/", response_model=List[CategoryModel])
def read_categories(limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category).limit(limit).all()
    return categories


@app.put("/categories/{category_id}", response_model=CategoryModel)
def update_category(
    category_id: int, new_category_name: str, db: Session = Depends(get_db)
):
    category_to_update = db.query(Category).filter_by(id=category_id).first()
    if category_to_update:
        category_to_update.name = new_category_name
        db.commit()
        db.refresh(category_to_update)
    return category_to_update


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_to_delete = db.query(Category).filter_by(id=category_id).first()
    if category_to_delete:
        db.delete(category_to_delete)
        db.commit()
    return f"Deleted category {category_to_delete}"


@app.get("/categories/{category_id}/exercises", response_model=List[ExerciseModel])
def read_all_exercises_in_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter_by(id=category_id).first()
    if category:
        return category.exercises


@app.post("/exercises/", response_model=ExerciseModel)
def create_exercise(exercise: ExerciseModel, db: Session = Depends(get_db)):
    new_exercise = Exercise(name=exercise.name, category_id=exercise.category_id)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise


@app.get("/exercises/", response_model=List[ExerciseModel])
def read_exercises(limit: int = 10, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).limit(limit).all()
    return exercises


@app.put("/exercises/{exercise_id}", response_model=ExerciseModel)
def update_exercise(
    exercise_id: int, exercise: ExerciseModel, db: Session = Depends(get_db)
):
    exercise_to_update = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise_to_update:
        exercise_to_update.name = exercise.name
        exercise_to_update.category_id = exercise.category_id
        db.commit()
        db.refresh(exercise_to_update)
    return exercise_to_update


@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_to_delete = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise_to_delete:
        db.delete(exercise_to_delete)
        db.commit()
    return f"exercise {exercise_to_delete} deleted"


@app.get("/exercises/{exercise_id}/entries", response_model=List[EntryModel])
def read_all_entries_for_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise:
        return exercise.entries


@app.post("/entries/", response_model=EntryModel)
def create_entry(entry: EntryModel, db: Session = Depends(get_db)):
    new_entry = Entry(
        time=datetime.now(),
        name=entry.name,
        set_info=entry.set_info,
        exercise_id=entry.exercise_id,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@app.get("/entries/", response_model=List[EntryModel])
def read_entries(limit: int = 10, db: Session = Depends(get_db)):
    entries = db.query(Entry).limit(limit).all()
    return entries


@app.put("/entries/{entry_id}", response_model=EntryModel)
def update_entry(entry_id: int, entry: EntryModel, db: Session = Depends(get_db)):
    entry_to_update = db.query(Entry).filter_by(id=entry_id).first()
    if entry_to_update:
        entry_to_update.time = datetime.now()
        entry_to_update.name = entry.name
        entry_to_update.set_info = entry.set_info
        entry_to_update.exercise_id = entry.exercise_id
        db.commit()
        db.refresh(entry_to_update)
    return entry_to_update


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry_to_delete = db.query(Entry).filter_by(id=entry_id).first()
    if entry_to_delete:
        db.delete(entry_to_delete)
        db.commit()
    return f"entry {entry_to_delete} deleted"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
