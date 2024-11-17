import unittest
import os
from src.library import Library
from src.book import Book
from src.member import Member

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book = Book("To Kill a Mockingbird", "Harper Lee")
        self.book1 = Book("1984", "George Orwell")
        self.book2 = Book("Brave New World", "Aldous Huxley")
        self.member = Member("Alice")

        self.library.add_book(self.book)
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_member(self.member)

        self.temp_file = "test_library.json"

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_add_book(self):
        new_book = Book("The Great Gatsby", "F. Scott Fitzgerald")
        response = self.library.add_book(new_book)
        self.assertIn(new_book, self.library.books)
        self.assertEqual(response, "Книга 'The Great Gatsby' добавлена в библиотеку.")

    def test_remove_book(self):
        response = self.library.remove_book("To Kill a Mockingbird")
        self.assertNotIn(self.book, self.library.books)
        self.assertEqual(response, "Книга 'To Kill a Mockingbird' удалена из библиотеки.")

    def test_find_irrelevant_book(self):
        book = self.library._find_book("Doom")
        self.assertIsNone(book)


    def test_save_to_file(self):
        response = self.library.save_to_file(self.temp_file)
        self.assertTrue(os.path.exists(self.temp_file))
        self.assertEqual(response, f"Информация сохранена в файл: {self.temp_file}.")

    def test_load_from_file(self):
        self.library.save_to_file(self.temp_file)

        new_library = Library()
        response = new_library.load_from_file(self.temp_file)

        self.assertEqual(response, f"Информация загружена из: {self.temp_file}.")
        self.assertEqual(len(new_library.books), 3)
        self.assertEqual(new_library.books[0].title, "To Kill a Mockingbird")
        self.assertEqual(new_library.members[0].name, "Alice")


if __name__ == "__main__":
    unittest.main()
