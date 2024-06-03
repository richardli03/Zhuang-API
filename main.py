from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry

def create_session(database_name):
    engine = create_engine(f"sqlite:///{database_name}.db")
    # have a completely new database every run
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def add_category(session: Session, name):
    category = Category(category_name=name)
    session.add(category)
    session.commit()
    return category

def add_entry(session: Session, time, recipient, amount, description, category_id):
    entry = Entry(time=time, recipient=recipient, amount=amount, description=description, category_id=category_id)
    session.add(entry)
    session.commit()
    return entry

def show_entries(session):
    entries = session.query(Entry).all()
    for entry in entries:
        print(f"Entry ID: {entry.id}, Amount: {entry.amount}, Recipient: {entry.recipient}, Category: {entry.category.name}")

def main():
    session = create_session("budget")
    category = add_category(session, "Travel")
    print("Category added:", category)

    entry_time = datetime.now()
    entry = add_entry(session, entry_time, "foo", 123.12, "bar", category_id=2)
    print("Entry added:", entry)
    show_entries(session)
    session.close()

if __name__ == "__main__":
    main()
