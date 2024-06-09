from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry
from library import *

def main():
    session = create_session("budget")
    travel = add_category(session, "Travel")
    food = add_category(session, "Food")
    rent = add_category(session, "Rent")
    print("Category added:", rent)

    entry_time = datetime.now()
    entry = add_entry(session, "foo", 123.12, "bar", category_id=rent.id, time = entry_time)
    entry = add_entry(session, "baz", 456.78, "qux", category_id=rent.id, time = entry_time)
    entry = add_entry(session, "abc", 901.23, "def", category_id=rent.id, time = entry_time)
    print("Entry added:", entry)
    
    show_entries(session)

    print(get_entry_category(session, 1))
    print(get_all_entries_in_category(session, "bbbb"))
    session.close()

if __name__ == "__main__":
    main()
