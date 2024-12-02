import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QGridLayout, QLineEdit, QLabel, QProgressBar, 
                             QTextEdit, QMessageBox, QComboBox, QSpinBox, 
                             QCheckBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class RandomWordGenerator:
    """
    Класс для генерации случайных слов и имен.
    """
    @staticmethod
    def generate_random_word(length):
        """
        Генерация случайного слова заданной длины.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_name():
        """
        Генерация случайного имени.
        """
        first_names = ["Алексей", "Мария", "Дмитрий", "Анна", "Сергей", "Екатерина", "Иван", "Ольга"]
        last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Попов", "Зайцев", "Лебедев"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    @staticmethod
    def generate_random_words(count, length):
        """
        Генерация списка случайных слов заданной длины.
        """
        return [RandomWordGenerator.generate_random_word(length) for _ in range(count)]

class WordGenerator(QWidget):
    """
    Класс для создания графического интерфейса генератора случайных слов.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор Случайных Слов")
        self.setGeometry(100, 100, 800, 600)

        font = QFont("Arial", 16)

        # Кнопки управления
        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)

        layout = QGridLayout()
        layout.addWidget(self.help_button, 0, 0)

        # Результат
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setFont(font)
        layout.addWidget(self.result, 1, 0, 1, 5)

        # Количество слов
        layout.addWidget(QLabel("Количество слов:"), 2, 0)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 100)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 2, 1)

        # Длина слов
        layout.addWidget(QLabel("Длина слов:"), 2, 2)
        self.length_input = QSpinBox()
        self.length_input.setRange(1, 20)
        self.length_input.setValue(5)
        layout.addWidget(self.length_input, 2, 3)

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_words)
        layout.addWidget(self.generate_button, 3, 0, 1, 5)

        self.setLayout(layout)

    def generate_words(self):
        """
        Генерация случайных слов и имен.
        """
        try:
            count = self.count_input.value()
            length = self.length_input.value()
            words = RandomWordGenerator.generate_random_words(count, length)
            result_text = f"Сгенерированные слова ({count} шт.):\n{words}"
            self.result.setText(result_text)
        except Exception as e:
            self.result.setText(f"Ошибка: {str(e)}")

    def show_help(self):
        """
        Показ справки.
        """
        QMessageBox.information(self, "Справка", 
            "Генератор случайных слов:\n"
            "1. Укажите количество и длину слов.\n"
            "2. Нажмите 'Сгенерировать' для получения результата.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = WordGenerator()
    generator.show()
    sys.exit(app.exec_())