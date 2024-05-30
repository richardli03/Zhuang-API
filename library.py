from enum import Enum, auto
from sqlalchemy import ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum

Base = declarative_base()

class Category(Enum):
    Income = auto()
    Food = auto()
    Transportation = auto()
    Entertainment = auto()
    Personal = auto()
    Misc = auto()
    

    
class Main(Base):
    __tablename__ = "main"

    id = Column("item_id", Integer, primary_key=True)
    name = Column("name", String)
    category = Column("category", Enum(Category))
    age = Column("age", Integer)

    def __init__(self, ssn, name, gender, age) -> None:
        self.ssn = ssn
        self.name = name
        self.gender = gender
        self.age = age
    def __repr__(self) -> str:
        return f"Person: {self.name}, ssn {self.ssn}"

# How to link databases
class Entry(Base):
    __tablename__ = "entries"
    
    tid = Column("tid", Integer, primary_key=True)
    desc = Column("description", String)
    owner = Column(Integer, ForeignKey("persons.ssn"))

    def __init__(self, tid, desc, owner) -> None:
        self.tid = tid
        self.desc = desc
        self.owner = owner

    def __repr__(self) -> str:
        return f"thing {self.tid} is owned by {self.owner}"
    

