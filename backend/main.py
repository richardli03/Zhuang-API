from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import uvicorn
from libs.db_utils import create_session
from typing import Union, List
from datetime import datetime
from libs.databases import Category, Exercise, Entry
from libs.schemas import *
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "general",
        "description": "General operations",
    },
    {
        "name": "entries",
        "description": "operate on entries",
    },
    {
        "name": "exercises",
        "description": "operate on specific exercises",
    },
    {
        "name": "categories",
        "description": "operate on categories",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

# allow react app to communicate w API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    session = create_session("richard_workouts")
    try:
        yield session
    finally:
        session.close()


@app.get("/", tags=["general"], response_class=PlainTextResponse)
def ping():
    return "ping"


@app.post("/categories/", response_model=CategoryOutput, tags=["categories"])
def create_category(category_name: str, db: Session = Depends(get_db)):
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/categories/", response_model=List[CategoryOutput], tags=["categories"])
def read_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@app.put(
    "/categories/{category_id}", response_model=CategoryOutput, tags=["categories"]
)
def update_category(
    category_id: int, new_category: CategoryInput, db: Session = Depends(get_db)
):
    category_to_update = db.query(Category).filter_by(id=category_id).first()
    if category_to_update:
        category_to_update.name = new_category.name
        db.commit()
        db.refresh(category_to_update)
    return category_to_update


@app.delete("/categories/{category_id}", tags=["categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_to_delete = db.query(Category).filter_by(id=category_id).first()
    if category_to_delete:
        db.delete(category_to_delete)
        db.commit()
    return f"Deleted category {category_to_delete}"


@app.get(
    "/categories/{category_id}/exercises",
    response_model=List[ExerciseOutput],
    tags=["exercises"],
)
def read_all_exercises_in_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter_by(id=category_id).first()
    if category:
        return category.exercises


@app.post("/exercises/", response_model=ExerciseOutput, tags=["exercises"])
def create_exercise(exercise: ExerciseInput, db: Session = Depends(get_db)):
    new_exercise = Exercise(name=exercise.name, category_id=exercise.category_id)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise


@app.get("/exercises/", response_model=List[ExerciseOutput], tags=["exercises"])
def read_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises


@app.put("/exercises/{exercise_id}", response_model=ExerciseOutput, tags=["exercises"])
def update_exercise(
    exercise_id: int, exercise: ExerciseInput, db: Session = Depends(get_db)
):
    exercise_to_update = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise_to_update:
        exercise_to_update.name = exercise.name
        exercise_to_update.category_id = exercise.category_id
        db.commit()
        db.refresh(exercise_to_update)
    return exercise_to_update


@app.delete("/exercises/{exercise_id}", tags=["exercises"])
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_to_delete = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise_to_delete:
        db.delete(exercise_to_delete)
        db.commit()
    return f"exercise {exercise_to_delete} deleted"


@app.get(
    "/exercises/{exercise_id}/entries",
    response_model=List[EntryOutput],
    tags=["entries"],
)
def read_all_entries_for_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter_by(id=exercise_id).first()
    if exercise:
        return exercise.entries


@app.post("/entries/", response_model=EntryOutput, tags=["entries"])
def create_entry(entry: EntryInput, db: Session = Depends(get_db)):
    exercise_id = db.query(Exercise).filter_by(name=entry.name).first().id
    new_entry = Entry(
        time=datetime.now(),
        exercise_id=exercise_id,
        set_info=entry.set_info,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@app.get("/entries/", response_model=List[EntryOutput], tags=["entries"])
def read_entries(db: Session = Depends(get_db)):
    entries = db.query(Entry).all()
    return entries


@app.put("/entries/{entry_id}", response_model=EntryOutput, tags=["entries"])
def update_entry(entry_id: int, entry: EntryInput, db: Session = Depends(get_db)):
    exercise_id = db.query(Exercise).filter_by(name=entry.name).first().id
    entry_to_update = db.query(Entry).filter_by(id=entry_id).first()
    if entry_to_update:
        entry_to_update.time = datetime.now()
        entry_to_update.set_info = entry.set_info
        entry_to_update.exercise_id = exercise_id
        db.commit()
        db.refresh(entry_to_update)
    return entry_to_update


@app.delete("/entries/{entry_id}", tags=["entries"])
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry_to_delete = db.query(Entry).filter_by(id=entry_id).first()
    if entry_to_delete:
        db.delete(entry_to_delete)
        db.commit()
    return f"entry {entry_to_delete} deleted"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
