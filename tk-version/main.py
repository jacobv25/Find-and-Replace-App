import re
import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox as messagebox

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.editor = scrolledtext.ScrolledText(self)
        self.editor.pack()

        self.cli = scrolledtext.ScrolledText(self)
        self.cli.bind('<Return>', self.execute_command)
        self.cli.pack()

        # Add a list to store replacements
        self.replacements = []

    def execute_command(self, event=None):
        # Get the last line in the CLI box
        command = self.cli.get('end-2c linestart', 'end-1c')

        if command.startswith("sr "):
            _, search_text, replace_text = command.split(" ", 2)

            # Check if search text is in the editor text
            text = self.editor.get(1.0, tk.END)
            if search_text not in text:
                self.cli.insert(tk.END, f"No matches for '{search_text}' found in text.\n")
                return

            # Replace text and update log
            new_text = self.preserve_case_replace(text, search_text, replace_text)
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, new_text)
            self.cli.insert(tk.END, f"Replaced '{search_text}' with '{replace_text}'\n")

            # Store the replacement
            self.replacements.append((search_text, replace_text))
        elif command == "reverse":
            # Reverse the obfuscation
            self.reverse_obfuscation()
        else:
            self.cli.insert(tk.END, f"Unknown command: {command}\n")

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

    def reverse_obfuscation(self):
        # Iterate over the replacements in reverse order
        text = self.editor.get(1.0, tk.END)
        for search_text, replace_text in reversed(self.replacements):
            # Replace the obfuscated text with the original text
            new_text = self.preserve_case_replace(text, replace_text, search_text)
            text = new_text

        # Update the editor and log
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, new_text)
        self.cli.insert(tk.END, " | Reversed obfuscation\n")


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
