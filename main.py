from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import uvicorn
from libs.db_utils import create_session
from typing import Union, List
from pydantic import BaseModel
from datetime import datetime
from libs.databases import Category, Entry

app = FastAPI()

class CategoryModel(BaseModel):
    name: str

class EntryModel(BaseModel):
    time: datetime
    recipient: str
    amount: float
    desc: str
    category_id: int

def get_db():
    session = create_session("budget")
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def read_root():
    return """Creating a budgetting application just to see if I can make a RESTful API"""

@app.post("/categories/", response_model=CategoryModel)
def create_category(category: CategoryModel, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[CategoryModel])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@app.post("/entries/", response_model=EntryModel)
def create_entry(entry: EntryModel, db: Session = Depends(get_db)):
    db_entry = Entry(time = entry.time, recipient=entry.recipient, amount=entry.amount, description=entry.desc, category_id=entry.category_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/entries/", response_model=List[EntryModel])
def read_entries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    entries = db.query(Entry).offset(skip).limit(limit).all()
    return entries

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
