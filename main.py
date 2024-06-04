from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry

def create_session(database_name):
    """Create a new database session and return it."""
    engine = create_engine(f"sqlite:///{database_name}.db")
    # have a completely new database every run
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session

def add_category(session: Session, name):
    """Add a new category to the database and return it."""
    category = Category(category_name=name)
    session.add(category)
    session.commit()
    return category

def add_entry(session: Session, time, recipient, amount, description, category_id):
    """Add a new entry to the database and return it."""
    entry = Entry(time=time, recipient=recipient, amount=amount, description=description, category_id=category_id)
    session.add(entry)
    session.commit()
    return entry

def show_entries(session):
    """Show all entries in the database"""
    entries = session.query(Entry).all()
    for entry in entries:
        print(f"Entry ID: {entry.id}, Amount: {entry.amount}, Recipient: {entry.recipient}, Category: {entry.category.name}")

def main():
    session = create_session("budget")
    category = add_category(session, "Travel")
    category = add_category(session, "Food")
    category = add_category(session, "Rent")
    print("Category added:", category)

    entry_time = datetime.now()
    entry = add_entry(session, entry_time, "foo", 123.12, "bar", category_id=1)
    entry = add_entry(session, entry_time, "baz", 456.78, "qux", category_id=3)
    print("Entry added:", entry)
    show_entries(session)
    session.close()

if __name__ == "__main__":
    main()
