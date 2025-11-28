import unittest
from pathlib import Path
from library_manager import LibraryInventory, Book


class TestLibraryInventory(unittest.TestCase):
    def setUp(self):
        # Use a temporary file in tests folder
        self.temp_path = Path("test_catalog.json")
        if self.temp_path.exists():
            self.temp_path.unlink()
        self.inventory = LibraryInventory(self.temp_path)

    def tearDown(self):
        if self.temp_path.exists():
            self.temp_path.unlink()

    def test_add_and_search_by_isbn(self):
        book = Book(title="Test Book", author="Me", isbn="123")
        self.inventory.add_book(book)
        found = self.inventory.search_by_isbn("123")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Test Book")


if __name__ == "__main__":
    unittest.main()