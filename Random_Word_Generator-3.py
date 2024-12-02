import sys
import random
import pymorphy2
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QGridLayout, QLineEdit, QLabel, QProgressBar, 
                            QTextEdit, QMessageBox, QComboBox, QSpinBox)

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
                layout.addWidget(QLabel("Длина слова/Количество:"), 3, 0)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 100)
        self.count_input.setValue(1)
        layout.addWidget(self.count_input, 3, 1)

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self.generate_words)
        layout.addWidget(self.generate_button, 4, 0, 1, 5)

        self.setLayout(layout)
        self.apply_theme()

    def generate_words(self):
        """
        Генерация случайных слов, словосочетаний или имен.
        """
        try:
            count = self.count_input.value()
            generation_type = self.generation_type.currentText()

            if generation_type == 'Случайные слова':
                words = [self.word_generator.generate_random_phrase(count) for _ in range(5)]
                result_text = f"Сгенерированы случайные слова:\n{words}"

            elif generation_type == 'Словосочетания':
                phrases = self.word_generator.generate_random_phrase(count)
                result_text = f"Сгенерированы словосочетания ({count} шт.):\n{phrases}"

            elif generation_type == 'Случайные имена':
                names = self.word_generator.generate_random_names(count)
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
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.theme_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.help_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.export_button.setStyleSheet("background-color: #4C4C4C; color: white;")
            self.result.setStyleSheet("background-color: #1E1E1E; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.theme_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.help_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.export_button.setStyleSheet("background-color: #CCCCCC; color: black;")
            self.result.setStyleSheet("background-color: #F0F0F0; color: black;")

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

class SplashScreen(QWidget):
    """
    Класс для отображения заставки при запуске приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #2E2E2E;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Логотип
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap
                            ("logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("opacity: 0;")
        layout.addWidget(self.logo)

        # Заголовок
        self.title = QLabel("")
        self.title.setAlignment(Qt.AlignCenter
                self.title.setStyleSheet("color: white; font-size: 50px; opacity: 0;")
        layout.addWidget(self.title)

        # Индикатор загрузки
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Кнопка с текстом
        self.footer_button = QPushButton('Создано Габеркорн Вадимом')
        self.footer_button.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;  
                color: black; 
                font-size: 18px; 
                font-weight: bold; 
                border: 2px solid #FFA500;  
                border-radius: 10px; 
                padding: 10px 20px;  
                max-width: 350px;   
            }
            QPushButton:hover {
                background-color: #FFA500;  
                border: 2px solid #FF8C00;  
            }
        """)
        self.footer_button.setFixedWidth(350)
        self.footer_button.setCursor(Qt.PointingHandCursor)

        layout.addStretch()
        layout.addWidget(self.footer_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

        # Анимация для логотипа
        self.logo_animation = QPropertyAnimation(self.logo, b"opacity")
        self.logo_animation.setDuration(2000)
        self.logo_animation.setStartValue(0)
        self.logo_animation.setEndValue(1)

        # Таймер для обновления индикатора загрузки
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

        self.show()
        self.logo_animation.start()

        # Инициализация анимации заголовка
        self.title_text = "RANDOM WORD GENERATOR"
        self.title_index = 0
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.update_title)
        self.title_timer.start(200)

    def update_title(self):
        """
        Обновление заголовка заставки.
        """
        if self.title_index < len(self.title_text):
            self.title.setText(self.title.text() + self.title_text[self.title_index])
            self.title_index += 1
        else:
            self.title_timer.stop()

        if self.title_index == len(self.title_text):
            self.title_animation = QPropertyAnimation(self.title, b"opacity")
            self.title_animation.setDuration(8000)
            self.title_animation.setStartValue(0)
            self.title_animation.setEndValue(1)
            self.title_animation.start()

    def update_progress(self):
        """
        Обновление индикатора загрузки.
        """
        value = self.progress.value() + 4
        if value > 100:
            self.timer.stop()
            self.close()
            self.open_generator()
        self.progress.setValue(value)

    def open_generator(self):
        """
        Открытие основного окна генератора случайных слов.
        """
        self.generator = RandomGenerator()
        self.generator.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    sys.exit(app.exec_())