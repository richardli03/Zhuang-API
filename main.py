from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry
from library import create_session, add_category, add_entry, show_entries

def main():
    session = create_session("budget")
    category = add_category(session, "Travel")
    category = add_category(session, "Food")
    category = add_category(session, "Rent")
    print("Category added:", category)

    entry_time = datetime.now()
    entry = add_entry(session, "foo", 123.12, "bar", category_id=1, time = entry_time)
    entry = add_entry(session, "baz", 456.78, "qux", category_id=3, time = entry_time)
    print("Entry added:", entry)
    show_entries(session)
    session.close()

if __name__ == "__main__":
    main()
