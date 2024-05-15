"""
Demonstrating how to create an engine and interact with sqlite using SQLAlchemy
"""
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base

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


engine = create_engine("sqlite:///testdb.db")
# have a completely new database every run
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind = engine)
session = Session()


# How to add values to the database
mike = Person(3, "mike", "m", 35)
paul = Person(2, "paul", "m", 25)
paul2 = Person(1, "paul", "m", 24)
session.add(mike)
session.add(paul)
session.add(paul2)
session.commit()

t1 = Thing(1, "Test1", mike.ssn)
t2 = Thing(2, "Test2", mike.ssn)
t3 = Thing(3, "Test3", paul.ssn)
session.add(t1)
session.add(t2)
session.add(t3)
session.commit()

# How to do queries
results = session.query(Person).all()
# print(results)

results = session.query(Person).filter(Person.name == "paul").all()



# More complex queries
results = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.name == "mike").all()

print(results)

