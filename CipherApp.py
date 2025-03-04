import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox
)
import random

class CipherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Шифрування (ПД-41 Ємельянов Владислав)')

        self.cipher_label = QLabel('Виберіть тип шифрування:')
        self.cipher_combo = QComboBox()
        self.cipher_combo.addItems([
            'Однобуквена заміна',
            'Гасловий шифр',
            'Шифр Віженера',
            'Шифр Плейфера',
            'Вертикальна перестановка'
        ])

        self.description_label = QLabel('')
        self.cipher_combo.currentIndexChanged.connect(self.update_description)

        self.text_label = QLabel('Введіть текст:')
        self.text_edit = QTextEdit()

        self.key_label = QLabel('Ключ:')
        self.key_edit = QTextEdit()
        self.key_edit.hide()
        self.key_label.hide()

        self.cipher_combo.currentIndexChanged.connect(self.update_key_visibility)

        self.run_button = QPushButton('Виконати')
        self.run_button.clicked.connect(self.run_cipher)

        self.result_label = QLabel('Результат:')
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)

        self.info_label = QLabel('')
        vbox = QVBoxLayout()
        vbox.addWidget(self.cipher_label)
        vbox.addWidget(self.cipher_combo)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.text_label)
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.key_label)
        vbox.addWidget(self.key_edit)
        vbox.addWidget(self.run_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.result_edit)
        vbox.addWidget(self.info_label)

        self.setLayout(vbox)
        self.update_description(0)

    def update_description(self, index):
        descriptions = [
            'Однобуквена заміна: Кожна літера замінюється іншою випадковою літерою.',
            'Гасловий шифр: Використовує ключове слово для створення нового алфавіту.',
            'Шифр Віженера: Багатоалфавітний шифр з використанням ключового слова.',
            'Шифр Плейфера: Шифрує пари літер за допомогою матриці 5x5.',
            'Вертикальна перестановка: Переставляє літери тексту у стовпцях відповідно до ключа.'
        ]
        self.description_label.setText(descriptions[index])

    def update_key_visibility(self, index):
        if index == 1 or index == 2 or index == 3 or index == 4:  # Гасловий, Віженер, Плейфер, Перестановка
            self.key_edit.show()
            self.key_label.show()
        else:
            self.key_edit.hide()
            self.key_label.hide()

    def run_cipher(self):
        cipher_type = self.cipher_combo.currentText()
        text = self.text_edit.toPlainText().upper()
        key = self.key_edit.toPlainText().upper()

        if cipher_type == 'Однобуквена заміна':
            result, info = self.single_substitution(text)
            self.result_edit.setPlainText(result)
            self.info_label.setText(f"Перемішаний алфавіт: {info}")
        elif cipher_type == 'Гасловий шифр':
            result, info = self.keyword_cipher(text, key)
            self.result_edit.setPlainText(result)
            self.info_label.setText(f"Ключовий алфавіт: {info}")
        elif cipher_type == 'Шифр Віженера':
            result, info = self.vigenere_cipher(text, key)
            self.result_edit.setPlainText(result)
            self.info_label.setText(f"Ключ: {info}")
        elif cipher_type == 'Шифр Плейфера':
            result, info = self.playfair_cipher(text, key)
            self.result_edit.setPlainText(result)
            self.info_label.setText(f"Матриця Плейфера: {info}")
        elif cipher_type == 'Вертикальна перестановка':
            result, info = self.vertical_transposition(text, key)
            self.result_edit.setPlainText(result)
            self.info_label.setText(f"Порядок стовпців: {info}")

    def single_substitution(self, text):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shuffled_alphabet = ''.join(random.sample(alphabet, len(alphabet)))
        result = ''.join(shuffled_alphabet[alphabet.find(char)] if char in alphabet else char for char in text)
        return result, shuffled_alphabet

    def keyword_cipher(self, text, keyword):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        key_alphabet = ''.join(sorted(set(keyword + alphabet), key=(keyword + alphabet).index))
        result = ''.join(key_alphabet[alphabet.find(char)] if char in alphabet else char for char in text)
        return result, key_alphabet

    def vigenere_cipher(self, text, key):
        key = key.upper()
        key_len = len(key)
        result = ''
        for i, char in enumerate(text):
            if char.isalpha():
                shift = ord(key[i % key_len]) - ord('A')
                shifted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result += shifted_char
            else:
                result += char
        return result, key

    def playfair_cipher(self, text, key):
        def create_matrix(key):
            key = key.upper().replace('J', 'I')
            matrix = []
            used_chars = []
            for char in key:
                if char.isalpha() and char not in used_chars:
                    matrix.append(char)
                    used_chars.append(char)
            for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
                if char not in used_chars:
                    matrix.append(char)
            return [matrix[i:i + 5] for i in range(0, 25, 5)]

        def find_char(matrix, char):
            for row_index, row in enumerate(matrix):
                if char in row:
                    return row_index, row.index(char)

        def encrypt_pair(matrix, pair):
            row1, col1 = find_char(matrix, pair[0])
            row2, col2 = find_char(matrix, pair[1])

            if row1 == row2:
                return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                return matrix[row1][col2] + matrix[row2][col1]

        matrix = create_matrix(key)
        text = text.replace('J', 'I')
        if len(text) % 2 != 0:
            text += 'X'

        pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
        result = ''.join(encrypt_pair(matrix, pair) for pair in pairs)
        return result, '\n'.join(' '.join(row) for row in matrix)

    def vertical_transposition(self, text, key):
        try:
            key_order = sorted(range(len(key)), key=lambda k: key[k])
            cols = [''] * len(key)
            for i, char in enumerate(text):
                cols[i % len(key)] += char
            result = ''.join(cols[i] for i in key_order)
            return result, key_order
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Невірний ключ: {e}")
            return "Помилка шифрування."

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec())