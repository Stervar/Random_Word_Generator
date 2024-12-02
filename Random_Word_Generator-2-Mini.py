import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QGridLayout, QLabel, QTextEdit, QMessageBox, 
                             QComboBox, QSpinBox)
from PyQt5.QtGui import QFont

class RandomWordGenerator:
    """
    Класс для генерации случайных слов и словосочетаний.
    """
    @staticmethod
    def generate_random_word(length):
        """
        Генерация случайного слова заданной длины.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_phrase(word_count):
        """
        Генерация случайного словосочетания.
        """
        nouns = ['кот', 'дом', 'стол', 'книга', 'город', 'друг', 'машина', 'солнце']
        adjectives = ['красный', 'большой', 'маленький', 'яркий', 'старый', 'новый', 'синий', 'зеленый']
        verbs = ['идет', 'читает', 'смеется', 'думает', 'работает', 'играет', 'танцует', 'поет']

        phrase_types = [
            lambda: f"{random.choice(adjectives)} {random.choice(nouns)}",
            lambda: f"{random.choice(nouns)} {random.choice(verbs)}",
            lambda: f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)}"
        ]

        return [random.choice(phrase_types)() for _ in range(word_count)]

    @staticmethod
    def generate_random_names(count):
        """
        Генерация случайных имен.
        """
        first_names = ["Алексей", "Мария", "Дмитрий", "Анна", "Сергей", "Екатерина", "Иван", "Ольга"]
        last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Попов", "Зайцев", "Лебедев"]
        return [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(count)]

class RandomGenerator(QWidget):
    """
    Класс для создания графического интерфейса генератора случайных слов.
    """
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.setWindowTitle("Генератор Случайных Слов")
        self.setGeometry(100, 100, 600, 500)
        self.history = []
        
        self.init_ui()

    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.
        """
        layout = QGridLayout()
        font = QFont("Arial", 12)

        # Кнопки управления
        self.theme_button = self.create_button("Светлая тема", self.toggle_theme)
        self.help_button = self.create_button("?", self.show_help)
        self.export_button = self.create_button("Экспорт", self.export_history)

        layout.addWidget(self.theme_button, 0, 0)
        layout.addWidget(self.help_button, 0, 1)
        layout.addWidget(self.export_button, 0, 2)

        # Результат
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Тип генерации
        layout.addWidget(QLabel("Тип генерации:"), 2, 0)
        self.generation_type = QComboBox()
        self.generation_type.addItems([
            'Случайные слова', 
            'Словосочетания', 
            'Случайные имена'
        ])
        layout.addWidget(self.generation_type, 2, 1)

        # Длина слова / количество
        layout.addWidget(QLabel("Длина слова/Количество:"), 3, 0)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 100)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 3, 1)

        # Кнопка генерации
        self.generate_button = self.create_button("Сгенерировать", self.generate_words)
        layout.addWidget(self.generate_button, 4, 0, 1, 5)

        self.setLayout(layout)
        self.apply_theme()

    def create_button(self, text, connection):
        """
        Создание кнопки с заданным текстом и обработчиком.
        """
        button = QPushButton(text)
        button.clicked.connect(connection)
        return button

    def generate_words(self):
        """
        Генерация случайных слов, словосочетаний или имен.
        """
        try:
            count = self.count_input.value()
            generation_type = self.generation_type.currentText()

            if generation_type == 'Случайные слова':
                words = [RandomWordGenerator.generate_random_word(count) for _ in range(5)]
                result_text = f"Сгенерированы случайные слова (длина {count}):\n{words}"

            elif generation_type == 'Словосочетания':
                phrases = RandomWordGenerator.generate_random_phrase(count)
                result_text = f"Сгенерированы словосочетания ({count} шт.):\n{phrases}"

            elif generation_type == 'Случайные имена':
                names = RandomWordGenerator.generate_random_names(count)
                result_text = f"Сгенерированы случайные имена ({count} шт.):\n{names}"

            self.result.setText(result_text)
            self.history.append(result_text)
        except Exception as e:
            self.result.setText(f"Ошибка: {str(e)}")

    def apply_theme(self):
        """
        Применение темы.
        """
        if self.is_dark_theme:
            self.setStyleSheet("""
                QWidget { background-color: #2E2E2E; color: white; }
                QPushButton { background-color: #4C4C4C; color: white; }
                QTextEdit { background-color: #1E1E1E; color: white; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #FFFFFF; color: black; }
                QPushButton { background-color: #CCCCCC; color: black; }
                QTextEdit { background-color: #F0F0F0; color: black; }
            """)

    def toggle_theme(self):
        """
        Переключение темы.
        """
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def show_help(self):
        """
        Показ справки.
        """
        QMessageBox.information(self, "Справка", 
            "Генератор случайных слов:\n"
            "1. Выберите тип генерации.\n"
            "2. Укажите длину слова или количество слов.\n"
            "3. Нажмите 'Сгенерировать' для получения результата.")

    def export_history(self):
        """
        Экспортировать историю генерации в текстовый файл.
        """
        with open("history.txt", "w") as file:
            for entry in self.history:
                file.write(entry + "\n")
        QMessageBox.information(self, "Экспорт", "История генерации экспортирована в history.txt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = RandomGenerator()
    generator.show()
    sys.exit(app.exec_()) 