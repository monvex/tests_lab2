import unittest
from src.member import Member
from src.book import Book

class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member("Alice")
        self.book = Book("The Catcher in the Rye", "J.D. Salinger")

    def test_borrow_book(self):
        response = self.member.borrow_book(self.book)
        self.assertIn(self.book, self.member.borrowed_books)
        self.assertEqual(response, "Книга 'The Catcher in the Rye' взята Alice.")
        self.assertFalse(self.book.available)

    def test_return_book(self):
        self.member.borrow_book(self.book)
        response = self.member.return_book(self.book)
        self.assertNotIn(self.book, self.member.borrowed_books)
        self.assertEqual(response, "Книга 'The Catcher in the Rye' возвращена Alice.")
        self.assertTrue(self.book.available)

    def test_return_not_borrowed_book(self):
        response = self.member.return_book(self.book)
        self.assertEqual(response, "Этот человек не брал заданную книгу.")

    def test_validate_data(self):
        with self.assertRaises(ValueError):
            invalid_member = Member("")
            invalid_member._validate_data()


if __name__ == "__main__":
    unittest.main()
