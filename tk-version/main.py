import re
import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox as messagebox

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.search_box = tk.Entry(self)
        self.search_box.insert(0, "Enter text to search...")

        self.replace_box = tk.Entry(self)
        self.replace_box.insert(0, "Enter replacement text...")

        self.log_box = scrolledtext.ScrolledText(self)

        self.search_label = tk.Label(self, text="Search Text")
        self.replace_label = tk.Label(self, text="Replacement Text")
        self.log_label = tk.Label(self, text="Log")

        self.editor = scrolledtext.ScrolledText(self)

        self.search_button = tk.Button(self, text="Search and Replace", command=self.search_and_replace)

        # Layout
        self.search_label.pack()
        self.search_box.pack()
        self.replace_label.pack()
        self.replace_box.pack()
        self.search_button.pack()
        self.editor.pack()
        self.log_label.pack()
        self.log_box.pack()

    def search_and_replace(self):
        search_text = self.search_box.get()
        replace_text = self.replace_box.get()

        # Replace text and update log
        text = self.editor.get(1.0, tk.END)
        new_text = self.preserve_case_replace(text, search_text, replace_text)
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, new_text)
        self.log_box.insert(tk.END, f"Replaced '{search_text}' with '{replace_text}'\n")

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


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
