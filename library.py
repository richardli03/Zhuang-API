from sqlalchemy import ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    ssn = Column("ssn", Integer, primary_key=True)
    name = Column("firstname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, name, gender, age) -> None:
        self.ssn = ssn
        self.name = name
        self.gender = gender
        self.age = age
    def __repr__(self) -> str:
        return f"Person: {self.name}, ssn {self.ssn}"

# How to link databases
class Thing(Base):
    __tablename__ = "things"
    tid = Column("tid", Integer, primary_key=True)
    desc = Column("description", String)
    owner = Column(Integer, ForeignKey("persons.ssn"))

    def __init__(self, tid, desc, owner) -> None:
        self.tid = tid
        self.desc = desc
        self.owner = owner

    def __repr__(self) -> str:
        return f"thing {self.tid} is owned by {self.owner}"
    

