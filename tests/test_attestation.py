import unittest
import os
from src.library import Library
from src.book import Book
from src.member import Member

class TestAttestation(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book = Book("To Kill a Mockingbird", "Harper Lee")


    def test_full_workflow(self):
        """Полный цикл: регистрация участника, добавление книги, выдача и возврат"""
        # Регистрация участника
        member = Member("Alice")
        add_member_response = self.library.add_member(member)
        self.assertIn("Пользователь 'Alice' добавлен в библиотеку.", add_member_response)

        # Поиск участника
        search_member_response = self.library._find_member("Alice")
        self.assertEqual(search_member_response.name, member.name)

        # Добавление книги
        book = Book("1984", "George Orwell")
        add_book_response = self.library.add_book(book)
        self.assertIn("Книга '1984' добавлена в библиотеку.", add_book_response)

        # Выдача книги участнику
        borrow_response = member.borrow_book(book)
        self.assertIn("Книга '1984' взята Alice.", borrow_response)
        self.assertFalse(book.available)

        # Возврат книги
        return_response = member.return_book(book)
        self.assertIn("Книга '1984' возвращена Alice.", return_response)
        self.assertTrue(book.available)

    def test_borrow_conflict(self):

        self.member1 = Member("Kate")
        self.member2 = Member("Bob")
        # Первый участник берет книгу
        borrow_response1 = self.member1.borrow_book(self.book)
        self.assertIn("Книга 'To Kill a Mockingbird' взята Kate.", borrow_response1)

        # Второй участник пытается взять ту же книгу
        borrow_response2 = self.member2.borrow_book(self.book)
        self.assertIn("Книга недоступна.", borrow_response2)

        # Проверяем, что книга по-прежнему принадлежит первому участнику
        self.assertEqual(self.book.borrower, "Kate")

    def test_user_find_book(self):

        self.library.add_book(Book("The War", "Guy"))
        self.library.add_book(Book("Wars", "Guy"))
        self.library.add_book(Book("WarStoke", "Guy"))
        self.library.add_book(Book("War Stakes", "Guy"))

        user_request1 = "War"
        suggestion1 = self.library.find_book(user_request1)

        self.assertIn(self.library.find_book("The War"), suggestion1)
        self.assertIn(self.library.find_book("Wars"), suggestion1)
        self.assertIn(self.library.find_book("WarStoke"), suggestion1)
        self.assertEqual(len(suggestion1), 3)


        user_request3 = "WarSto"
        suggestion3 = self.library.find_book(user_request3)

        self.assertIn(self.library.find_book("Wars"), suggestion3)
        self.assertIn(self.library.find_book("WarStoke"), suggestion3)
        self.assertIn(self.library.find_book("War Stakes"), suggestion3)
        self.assertEqual(len(suggestion1), 3)

        user_request4 = "WarStoke"
        suggestion4 = self.library.find_book(user_request4)

        self.assertEqual(suggestion4, self.library.find_book("WarStoke"))








if __name__ == "__main__":
    unittest.main()
