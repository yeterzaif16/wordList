import random
from cgitb import grey

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPalette, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QLabel, QPushButton, QMenu, QMessageBox, \
    QInputDialog
from wordlist import Word, insert_word, load_words


class MainWindow(QWidget):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.current_level = None

        self.layout = QVBoxLayout()

        self.level_layout = QHBoxLayout()
        self.radio_easy = QRadioButton("Easy")
        self.radio_medium = QRadioButton("Medium")
        self.radio_hard = QRadioButton("Hard")
        self.level_layout.addWidget(self.radio_easy)
        self.level_layout.addWidget(self.radio_medium)
        self.level_layout.addWidget(self.radio_hard)

        self.radio_easy.toggled.connect(lambda: self.set_level("easy"))
        self.radio_medium.toggled.connect(lambda: self.set_level("medium"))
        self.radio_hard.toggled.connect(lambda: self.set_level("hard"))

        self.layout.addLayout(self.level_layout)

        self.label_word = QLabel()
        self.label_word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_word)

        self.label_meaning = QLabel()
        self.label_meaning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_meaning)

        self.button_show_meaning = QPushButton("Show Meaning")
        self.button_show_meaning.clicked.connect(self.show_meaning)
        self.layout.addWidget(self.button_show_meaning)

        self.button_next = QPushButton("Next Word")
        self.button_next.clicked.connect(self.show_random_word)
        self.layout.addWidget(self.button_next)

        self.menu = QMenu()
        self.menu_insert_word = QAction("Insert Word", self)
        self.menu.addAction(self.menu_insert_word)
        self.menu_insert_word.triggered.connect(self.insert_word_dialog)

        self.button_menu = QPushButton('Menu')
        self.button_menu.setMenu(self.menu)
        self.layout.addWidget(self.button_menu)

        self.setLayout(self.layout)

        self.show_random_word()

        self.setup_styles()

        self.set_application_style()

    def setup_styles(self):
        self.label_word.setStyleSheet("""
            QLabel {
                 color: white;
                 font-size: 50px;
                 font-weight: bold;
                 font-family: "Gabriola";
                 }
         """)

        self.label_meaning.setStyleSheet("""
            QLabel {color: #303154;
            font-size: 50px; 
            font-family:"Segoe Print";
            }
            """)
        self.button_show_meaning.setStyleSheet("""
            QPushButton {
                background-color: #7b86ba;
                font-size: 50px;
            }
        """)

        self.button_next.setStyleSheet("""
                QPushButton {
                    background-color: yellow;
                    font-size: 50px;
                    }
        """)

        self.button_menu.setStyleSheet("""
                QPushButton {
                    background-color: #513552 ;
                    font-size: 50px;
                            }
        """)

    def set_application_style(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(86, 117, 120))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(11, 13, 12))
        self.setPalette(palette)


    def set_level(self, level):
        self.current_level = level
        self.show_random_word()

    def show_meaning(self):
        if hasattr(self, 'word'):
            self.label_meaning.setText(self.word.meaning)
        else:
            QMessageBox.warning(self, "Warning", "No word to show meaning.")

    def show_random_word(self):
        if self.current_level:
            level_words = [word for word in self.words if word.level == self.current_level]
            if level_words:
                self.word = random.choice(level_words)
                self.label_word.setText(self.word.word)
                self.label_meaning.clear()
            else:
                QMessageBox.warning(self, "Warning", f"No word found for level: {self.current_level}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a difficulty level")

    def insert_word_dialog(self, meaning):
        word, ok = QInputDialog.getText(self, 'Insert Word', 'Enter Word:')
        if ok and word:
            meaning, ok = QInputDialog.getText(self, 'Insert Word', 'Enter Meaning:')
            if ok and meaning:
                level, ok = QInputDialog.getItem(self, 'Insert Word', "Select Level:", ['easy', 'medium', 'hard'], 0, False)
                if ok:
                    new_word = Word(word, meaning, level)
                    insert_word(new_word)
                    self.words = load_words()
                    self.show_random_word()





