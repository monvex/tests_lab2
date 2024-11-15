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

        self.member1 = Member("Kate")
        self.member2 = Member("Bob")

        self.library.add_book(self.book)
        self.library.add_member(self.member1)
        self.library.add_member(self.member2)

        self.library.add_book(self.book)
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_member(self.member)

        self.member.borrow_book(self.book1)

        self.temp_file = "test_library.json"

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)


    def test_borrow_and_return_book(self):
        # Выдача книги
        borrow_response = self.member.borrow_book(self.book)
        self.assertIn("Книга 'To Kill a Mockingbird' взята Alice.", borrow_response)
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrower, "Alice")

        # Возврат книги
        return_response = self.member.return_book(self.book)
        self.assertIn("Книга 'To Kill a Mockingbird' возвращена Alice.", return_response)
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrower)

    def test_borrow_conflict(self):
        # Первый участник берет книгу
        borrow_response1 = self.member1.borrow_book(self.book)
        self.assertIn("Книга 'To Kill a Mockingbird' взята Kate.", borrow_response1)

        # Второй участник пытается взять ту же книгу
        borrow_response2 = self.member2.borrow_book(self.book)
        self.assertIn("Книга недоступна.", borrow_response2)

        # Проверяем, что книга по-прежнему принадлежит первому участнику
        self.assertEqual(self.book.borrower, "Kate")

    def test_borrow_deleted_book(self):

        # Удалить книгу из библиотеки
        remove_response = self.library.remove_book("1984")
        self.assertIn("Книга '1984' удалена из библиотеки.", remove_response)

        # Убедиться, что книга больше не доступна
        self.assertNotIn(self.book1, self.library.books)

        # Участник берет книгу
        borrow_response = self.member.borrow_book(self.book1)
        self.assertIn("Книга недоступна.", borrow_response)

    def test_return_unborrowed_book(self):
        # Попытка вернуть книгу, которая не была взята
        return_response = self.member.return_book(self.book)
        self.assertIn("Этот человек не брал заданную книгу.", return_response)
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrower)



if __name__ == "__main__":
    unittest.main()