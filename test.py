"""
Demonstrating how to create an engine and interact with sqlite using SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from library import Base, Thing, Person

def create_session():
    engine = create_engine("sqlite:///testdb.db")
    # have a completely new database every run
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def main(session: Session):
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
    results = session.query(Person).filter(Person.name == "paul").all()
    results = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.name == "mike").all()

    print(results)



if __name__ == "__main__":
    session = create_session()
    main(session)
    