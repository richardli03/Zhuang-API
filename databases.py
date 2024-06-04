from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
    
class Category(Base):
    __tablename__ = "categories"

    id = Column("id", Integer, primary_key=True, index = True, autoincrement= True)
    name = Column("name", String, unique = True)
    entries = relationship("Entry", back_populates="category")

    def __init__(self, category_name) -> None:
        self.name = category_name
        
    def __repr__(self) -> str:
        return f"Category: {self.name}, ID: {self.id}"
    
class Entry(Base):
    __tablename__ = "entries"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, index=True)
    recipient = Column ("recipient", String)
    amount = Column("amount", Float)
    desc = Column("description", String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="entries")

    def __init__(self, time, recipient, amount, description, category_id) -> None:
        self.time = time
        self.recipient = recipient
        self.amount = amount
        self.desc = description
        self.category_id = category_id


    def __repr__(self) -> str:
        return f"Entry {self.id} is for {self.amount} to {self.recipient}"
    

