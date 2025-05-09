import tkinter as tk
from tkinter import ttk

class TextEditor:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Edytor")
        self.frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Konfiguracja rozmiarów
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.setup_editor()
        
    def setup_editor(self):
        self.editor = tk.Text(self.frame, wrap=tk.WORD)
        self.editor.pack(fill=tk.BOTH, expand=True)
        
    def get_content(self):
        return self.editor.get('1.0', tk.END)
        
    def set_content(self, content):
        self.editor.delete('1.0', tk.END)
        self.editor.insert('1.0', content)
        
    def grid(self, **kwargs):
        self.frame.grid(**kwargs) 