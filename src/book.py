class Book:
    def __init__(self, title, author):
        self.title: str = title
        self.author: str = author
        self.available: bool = True
        self.borrower: str | None = None

    def get_info(self):
        """Возвращает информацию о книге."""
        return f"{self.title} by {self.author}"



    def change_status(self, status, borrower=None):
        """Меняет статус доступности книги и записывает заемщика, если книга взята."""
        self.available = status
        self.borrower = borrower if not status else None
        return "Статус изменен."

    def _validate_data(self):
        """Protected: Проверяет корректность данных книги."""
        if not self.title or not self.author:
            raise ValueError("Название и автор книги должны быть указаны!")


if __name__ == "__main__":
    book = Book()

    print(book.get_info())