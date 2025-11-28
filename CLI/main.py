# cli/main.py

import logging
import sys
from pathlib import Path

# --- Ensure project root on sys.path (so 'library_manager' is importable) ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from library_manager import Book, LibraryInventory


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def get_catalog_path():
    # catalog.json in project root (one level above /cli/)
    return ROOT_DIR / "catalog.json"


def read_menu_choice():
    """Read menu option safely (1–6)."""
    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 1 <= choice <= 6:
                return choice
        except ValueError:
            pass
        print("Invalid choice. Please enter a number between 1 and 6.")


def add_book_cli(inventory):
    print("\n--- Add Book ---")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()

    if not title or not author or not isbn:
        print("All fields are required.")
        return

    book = Book(title, author, isbn)
    inventory.add_book(book)
    inventory.save_to_file()
    print("Book added.")


def issue_book_cli(inventory):
    print("\n--- Issue Book ---")
    isbn = input("Enter ISBN: ").strip()
    book = inventory.search_by_isbn(isbn)
    if book is None:
        print("Book not found.")
        return

    if book.issue():
        inventory.save_to_file()
        print("Book issued.")
    else:
        print("Book is already issued.")


def return_book_cli(inventory):
    print("\n--- Return Book ---")
    isbn = input("Enter ISBN: ").strip()
    book = inventory.search_by_isbn(isbn)
    if book is None:
        print("Book not found.")
        return

    if book.return_book():
        inventory.save_to_file()
        print("Book returned.")
    else:
        print("Book was not issued.")


def view_all_cli(inventory):
    print("\n--- All Books ---")
    books = inventory.display_all()
    if not books:
        print("No books in catalog.")
    else:
        for i, book in enumerate(books, start=1):
            print(f"{i}. {book}")


def search_cli(inventory):
    print("\n--- Search ---")
    print("1. Search by Title")
    print("2. Search by ISBN")

    while True:
        try:
            choice = int(input("Enter choice (1-2): ").strip())
            if choice in (1, 2):
                break
        except ValueError:
            pass
        print("Please enter 1 or 2.")

    if choice == 1:
        query = input("Enter title or part of title: ").strip()
        results = inventory.search_by_title(query)
        if not results:
            print("No matching books found.")
        else:
            print(f"Found {len(results)} book(s):")
            for book in results:
                print(book)
    else:
        isbn = input("Enter ISBN: ").strip()
        book = inventory.search_by_isbn(isbn)
        if book is None:
            print("No book found with that ISBN.")
        else:
            print("Book found:")
            print(book)


def main():
    setup_logging()
    catalog_path = get_catalog_path()
    inventory = LibraryInventory(catalog_path)

    while True:
        print("\n===== Library Inventory Manager =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search")
        print("6. Exit")

        choice = read_menu_choice()

        if choice == 1:
            add_book_cli(inventory)
        elif choice == 2:
            issue_book_cli(inventory)
        elif choice == 3:
            return_book_cli(inventory)
        elif choice == 4:
            view_all_cli(inventory)
        elif choice == 5:
            search_cli(inventory)
        elif choice == 6:
            print("Exiting... Bye!")
            break


if __name__ == "__main__":
    main()