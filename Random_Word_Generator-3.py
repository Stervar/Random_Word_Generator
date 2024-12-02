import sys
import random
import pymorphy2
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QGridLayout, QLineEdit, QLabel, QProgressBar, 
                             QTextEdit, QMessageBox, QComboBox, QSpinBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation

class ExtendedRandomWordGenerator:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        
        # Загрузка максимально полных словарей
        self.nouns = self._load_words('noun')
        self.adjectives = self._load_words('adjf')
        self.verbs = self._load_words('verb')
        self.first_names = self._load_first_names()
        self.last_names = self._load_last_names()

    def _load_words(self, pos):
        """
        Загрузка слов определенной части речи
        """
        words = set()
        with open('/usr/share/dict/russian', 'r', encoding='utf-8') as f:
            for word in f:
                word = word.strip().lower()
                parse = self.morph.parse(word)[0]
                if parse.tag.POS == pos:
                    words.add(word)
        return list(words)

    def _load_first_names(self):
        """
        Загрузка полного списка имен
        """
        names = []
        with open('russian_names.txt', 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f]
        return names

    def _load_last_names(self):
        """
        Загрузка полного списка фамилий
        """
        last_names = []
        with open('russian_surnames.txt', 'r', encoding='utf-8') as f:
            last_names = [line.strip() for line in f]
        return last_names

    def generate_random_phrase(self, word_count):
        """
        Генерация случайных словосочетаний с использованием полных словарей
        """
        phrases = []
        for _ in range(word_count):
            phrase_types = [
                lambda: f"{random.choice(self.adjectives)} {random.choice(self.nouns)}",
                lambda: f"{random.choice(self.nouns)} {random.choice(self.verbs)}",
                lambda: f"{random.choice(self.adjectives)} {random.choice(self.nouns)} {random.choice(self.verbs)}"
            ]
            phrases.append(random.choice(phrase_types)())
        return phrases

    def generate_random_names(self, count):
        """
        Генерация случайных имен с полным списком
        """
        return [f"{random.choice(self.first_names)} {random.choice(self.last_names)}" for _ in range(count)]

class RandomGenerator(QWidget):
    """
    Класс для создания графического интерфейса генератора случайных слов.
    """
    def __init__(self):
        super().__init__()
        self.word_generator = ExtendedRandomWordGenerator()  # Инициализация расширенного генератора слов
        self.is_dark_theme = True
        self.setWindowTitle("Генератор Случайных Слов")
        self.setGeometry(100, 100, 800, 800)

        self.history = []
        font = QFont("Arial", 16)

        # Кнопки управления
        self.theme_button = QPushButton("Светлая тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)

        self.export_button = QPushButton("Экспорт")
        self.export_button.clicked.connect(self.export_history)

        layout = QGridLayout()
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
        layout.addWidget(QLabel("Длина слова/