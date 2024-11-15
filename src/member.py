from src.book import Book


class Member:
    def __init__(self, name):
        self.name: str = name
        self.borrowed_books: list[Book] = []

    def borrow_book(self, book: Book):
        """Добавляет книгу к списку заимствованных книг участника."""
        if book.available:
            self.borrowed_books.append(book)
            book.change_status(False, self.name)
            return f"Книга '{book.title}' взята {self.name}."
        else:
            return "Книга недоступна."

    def return_book(self, book):
        """Возвращает книгу, убирая ее из списка заимствованных."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.change_status(True)
            return f"Книга '{book.title}' возвращена {self.name}."
        else:
            return "Этот человек не брал заданную книгу."


    def _validate_data(self):
        """Protected: Проверяет корректность данных пользователя."""
        if not self.name:
            raise ValueError("Имя пользователя должно быть указано!")
