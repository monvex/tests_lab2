import unittest
import os
from src.library import Library
from src.book import Book
from src.member import Member

class TestIntegration(unittest.TestCase):
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


    def test_borrow_and_check_borrower(self):
        # Выдача книги
        borrow_response = self.member.borrow_book(self.book)
        self.assertIn("Книга 'To Kill a Mockingbird' взята Alice.", borrow_response)
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrower, "Alice")

    def test_return_and_check_borrower(self):
        # Выдача книги
        borrow_response = self.member.return_book(self.book1)
        self.assertIn("Книга '1984' возвращена Alice.", borrow_response)
        self.assertTrue(self.book1.available)
        self.assertIsNone(self.book1.borrower)

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

    def test_save_and_restore_with_active_loans(self):
        """Интеграционный тест: сохранение и восстановление с активными действиями"""

        # Участник берет одну книгу
        self.member.borrow_book(self.book1)

        # Сохранение состояния
        save_response = self.library.save_to_file(self.temp_file)
        self.assertIn("Информация сохранена в файл: test_library.json.", save_response)

        # Создание новой библиотеки и загрузка данных
        new_library = Library()
        load_response = new_library.load_from_file(self.temp_file)
        self.assertIn("Информация загружена из: test_library.json.", load_response)

        # Проверка восстановленного состояния
        restored_book1 = next((b for b in new_library.books if b.title == "1984"), None)
        restored_book2 = next((b for b in new_library.books if b.title == "Brave New World"), None)
        restored_member = next((m for m in new_library.members if m.name == "Alice"), None)

        self.assertIsNotNone(restored_book1)
        self.assertIsNotNone(restored_book2)
        self.assertIsNotNone(restored_member)

        self.assertFalse(restored_book1.available)
        self.assertEqual(restored_book1.borrower, "Alice")
        self.assertTrue(restored_book2.available)


    def test_suggest_add_suggest_book(self):

        user_request = "To Kill a Mocking"

        suggestions1 = self.library.suggest_books(user_request)

        self.library.add_book(Book("To Kill a Mocking guy", "Guy"))

        suggestions2 = self.library.suggest_books(user_request)

        self.assertLess(len(suggestions1), len(suggestions2))



if __name__ == "__main__":
    unittest.main()