from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from databases import Base, Category, Entry
from library import *

def main():
    session = create_session("budget", True)

    travel = add_category(session, "Travel")
    food = add_category(session, "Food")
    rent = add_category(session, "Rent")
    # rent = Category(category_name="Rent")
    print("Category added:", rent)



    entry_time = datetime.now()
    entry = add_entry(session, "foo", 123.12, "bar", category_id=rent.id, time = entry_time)
    entry = add_entry(session, "baz", 456.78, "qux", category_id=rent.id, time = entry_time)
    entry = add_entry(session, "abc", 901.23, "def", category_id=rent.id, time = entry_time)
    print("Entry added:", entry)
    
    show_entries(session)

    print(get_entry_category(session, 1))
    all_rent_entries = get_all_entries_in_category(session, "Rent")
    final_sum = 0 
    for entry in all_rent_entries:
        final_sum += entry.amount

    print(f"The amount of money you've spent on Rent is {final_sum}")
    
    session.close()

if __name__ == "__main__":
    main()
