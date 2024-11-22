import json
from src.book import Book
from src.member import Member
class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def _levenshtein_distance(self, s1: str, s2: str):
        """
        Вычисляет расстояние Левенштейна между двумя строками.

        Параметры:
        - s1 (str): Первая строка.
        - s2 (str): Вторая строка.

        Возвращает:
        - int: Расстояние Левенштейна между строками.
        """
        # Создаем матрицу размером (len(s1) + 1) x (len(s2) + 1)
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Заполняем первую строку и первый столбец
        for i in range(m + 1):
            dp[i][0] = i  # Удаление всех символов s1
        for j in range(n + 1):
            dp[0][j] = j  # Добавление всех символов s2

        # Заполняем матрицу
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:  # Если символы совпадают, не увеличиваем стоимость
                    cost = 0
                else:  # Если символы не совпадают, замена стоит 1
                    cost = 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Удаление
                    dp[i][j - 1] + 1,  # Вставка
                    dp[i - 1][j - 1] + cost  # Замена
                )

        return dp[m][n]

    def add_book(self, book):
        """Добавляет книгу в библиотеку."""
        self.books.append(book)
        return f"Книга '{book.title}' добавлена в библиотеку."

    def remove_book(self, title):
        """Удаляет книгу из библиотеки по названию."""
        book = self.find_book(title)
        if book:
            book.available = False
            book.borrower = None
            self.books.remove(book)
            return f"Книга '{title}' удалена из библиотеки."
        return "Книга не найдена."

    def add_member(self, member):
        """Добавляет участника в библиотеку."""
        if member.name in self.members:
            return f"Пользователь с именем'{member.name}' добавлен в библиотеку."
        self.members.append(member)
        return f"Пользователь '{member.name}' добавлен в библиотеку."

    def find_book(self, title):
        """Protected: Ищет книгу по названию."""
        for book in self.books:
            if book.title == title:
                return book

        suggestions = self.suggest_books(title)

        if (len(suggestions) > 0):
            return suggestions

        return None

    def _find_member(self, name):
        """Protected: Ищет человека по имени."""
        for member in self.members:
            if member.name == name:
                return member
        return None

    def suggest_books(self, title) -> list:
        """Предлагает похожие книги на основе расстояния Левенштейна."""
        suggestions = []
        for book in self.books:
            # Рассчитываем расстояние Левенштейна для каждого названия книги
            distance = self._levenshtein_distance(title.lower(), book.title.lower())
            if distance < 5:  # Порог, при котором мы считаем название похожим
                suggestions.append(book)
        return suggestions

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
                for book in self.books
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

        self.books = [
            Book(book["title"], book["author"])
            for book in data["books"]
        ]
        for book, book_data in zip(self.books, data["books"]):
            book.available = book_data["available"]
            book.borrower = book_data["borrower"]

        self.members = [
            Member(member["name"])
            for member in data["members"]
        ]
        for member, member_data in zip(self.members, data["members"]):
            member.borrowed_books = [
                self.find_book(title) for title in member_data["borrowed_books"]
            ]
        return f"Информация загружена из: {filepath}."

