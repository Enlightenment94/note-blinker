import os
from tkinter import filedialog

class FileOperations:
    @staticmethod
    def export_to_file(content, default_extension=".txt"):
        file_path = filedialog.asksaveasfilename(
            defaultextension=default_extension,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        return False
        
    @staticmethod
    def import_from_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
            return os.path.basename(file_path), content
        return None, None 