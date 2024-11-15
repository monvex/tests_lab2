import json
from src.book import Book
from src.member import Member

class Library:
    def __init__(self):
        self.collection = []
        self.members = []

    def add_book(self, book):
        """Добавляет книгу в библиотеку."""
        self.collection.append(book)
        return f"Книга '{book.title}' добавлена в библиотеку."

    def remove_book(self, title):
        """Удаляет книгу из библиотеки по названию."""
        book = self._find_book(title)
        if book:
            self.collection.remove(book)
            return f"Книга '{title}' удалена из библиотеки."
        return "Книга не найдена."

    def add_member(self, member):
        """Добавляет участника в библиотеку."""
        self.members.append(member)
        return f"Пользователь '{member.name}' добавлен в библиотеку."

    def _find_book(self, title):
        """Protected: Ищет книгу по названию."""
        for book in self.collection:
            if book.title == title:
                return book
        return None

    def save_to_file(self, filepath):
        """Сохраняет библиотеку и участников в JSON-файл."""
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "available": book.available,
                    "borrower": book.borrower,
                }
                for book in self.collection
            ],
            "members": [
                {
                    "name": member.name,
                    "borrowed_books": [book.title for book in member.borrowed_books],
                }
                for member in self.members
            ],
        }
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
        return f"Информация сохранена в файл: {filepath}."

    def load_from_file(self, filepath):
        """Загружает библиотеку и участников из JSON-файла."""
        with open(filepath, "r") as file:
            data = json.load(file)

        self.collection = [
            Book(book["title"], book["author"])
            for book in data["books"]
        ]
        for book, book_data in zip(self.collection, data["books"]):
            book.available = book_data["available"]
            book.borrower = book_data["borrower"]

        self.members = [
            Member(member["name"])
            for member in data["members"]
        ]
        for member, member_data in zip(self.members, data["members"]):
            member.borrowed_books = [
                self._find_book(title) for title in member_data["borrowed_books"]
            ]
        return f"Информация загружена из: {filepath}."
