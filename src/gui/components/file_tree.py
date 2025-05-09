import tkinter as tk
from tkinter import ttk
import os

class FileTree:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Drzewo notatek")
        self.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Konfiguracja rozmiarów
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.setup_tree()
        self.setup_buttons()
        
    def setup_tree(self):
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Podpięcie zdarzenia wyboru
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
    def setup_buttons(self):
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Dodaj folder", command=self.add_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Usuń", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        
    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            item_path = self.tree.item(item_id)['values'][0]
            
            # Sprawdź czy to plik
            if not os.path.isdir(item_path):
                # Przekaż ścieżkę pliku do głównej aplikacji
                if hasattr(self, 'on_file_selected'):
                    self.on_file_selected(item_path)
        
    def add_folder(self):
        pass
        
    def delete_item(self):
        pass
        
    def grid(self, **kwargs):
        self.frame.grid(**kwargs) 