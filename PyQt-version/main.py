import re
import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QTextBrowser
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        # Set some initial properties of the text edit widget
        self.setAcceptRichText(False)
        self.setPlaceholderText("Enter your code here...")

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter text to search...")

        self.replace_box = QLineEdit()
        self.replace_box.setPlaceholderText("Enter replacement text...")

        self.log_box = QTextBrowser()

        self.search_label = QLabel("Search Text")
        self.replace_label = QLabel("Replacement Text")
        self.log_label = QLabel("Log")

        self.editor = CodeEditor()

        self.search_button = QPushButton("Search and Replace")
        self.search_button.clicked.connect(self.search_and_replace)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.replace_label)
        self.layout.addWidget(self.replace_box)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.log_label)
        self.layout.addWidget(self.log_box)

        self.setLayout(self.layout)

    def search_and_replace(self):
        search_text = self.search_box.text()
        replace_text = self.replace_box.text()

        # Replace text and update log
        text = self.editor.toPlainText()
        new_text = self.preserve_case_replace(text, search_text, replace_text)
        self.editor.setPlainText(new_text)
        self.log_box.append(f"Replaced '{search_text}' with '{replace_text}'")

        # Highlight replace text
        self.highlight_text(replace_text)
        
        # # Clear highlights
        # self.editor.selectAll()
        # self.editor.mergeCurrentCharFormat(QTextCharFormat())

    def highlight_text(self, replace_text):
        self.editor.moveCursor(QTextCursor.Start)
        format = QTextCharFormat()
        format.setBackground(QColor("yellow"))

        while self.editor.find(replace_text):
            self.editor.textCursor().mergeCharFormat(format)

    def preserve_case_replace(self, original_text, search_text, replace_text):
        pattern = re.compile(re.escape(search_text), re.IGNORECASE)

        def replacer(match):
            s = match.group()
            if s.isupper():
                return replace_text.upper()
            elif s.islower():
                return replace_text.lower()
            elif s[0].isupper():
                return replace_text.capitalize()
            else:
                return replace_text

        return pattern.sub(replacer, original_text)

def main():
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
