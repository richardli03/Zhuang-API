from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry
from os.path import isfile

def create_session(database_name, make_new = False):
    """Create a new database session and return it."""
    database_path = f"sqlite:///{database_name}.db"
    if isfile(database_path):
        pass
    else:
        engine = create_engine(database_path)

    if make_new:
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

def add_entry(session: Session, recipient, amount, description, category_id, time = datetime.now()):
    """Add a new entry to the database and return it."""
    entry = Entry(time=time, recipient=recipient, amount=amount, description=description, category_id=category_id)
    session.add(entry)
    session.commit()
    return entry

def get_all_entries_in_category(session: Session, category_name):
    """_summary_

    Args:
        session (Session): _description_
        category_name (_type_): _description_
    """
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        return category.entries
    
    raise UserWarning(f"The category '{category_name}' does not exist")

def get_entry_category(session: Session, entry_id):
    """Given an entry id, return the name of the category it belongs to

    Args:
        session (Session): _description_
        entry_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return session.query(Category.name).join(Entry).filter(Entry.id == entry_id).scalar()

def show_entries(session):
    """Show all entries in the database"""
    entries = session.query(Entry).all()
    for entry in entries:
        print(f"Entry ID: {entry.id}, Amount: {entry.amount}, Recipient: {entry.recipient}, Category: {entry.category.name}")
