# tests/test_book.py

import unittest
from src.book import Book

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("1984", "George Orwell")

    def test_get_info(self):
        self.assertEqual(self.book.get_info(), "1984 by George Orwell")

    def test_change_status(self):
        response = self.book.change_status(False, "Alice")
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrower, "Alice")
        self.assertEqual(response, "Статус изменен.")

    def test_validate_data(self):
        with self.assertRaises(ValueError):
            invalid_book = Book("", "")
            invalid_book._validate_data()


if __name__ == "__main__":
    unittest.main()
