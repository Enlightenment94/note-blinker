import tkinter as tk
from tkinter import ttk, filedialog
import os

class Navbar:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.setup_buttons()
        
    def setup_buttons(self):
        # Przyciski nawigacyjne
        ttk.Button(self.frame, text="Otwórz folder", command=self.open_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="Zapisz", command=self.save_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="Cofnij", command=self.undo).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="Przywróć", command=self.redo).pack(side=tk.LEFT, padx=5)
        
    def open_folder(self):
        # Pobierz ścieżkę do folderu nadrzędnego
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        default_path = os.path.join(parent_dir, "mynote")
        
        folder_path = filedialog.askdirectory(
            initialdir=default_path,
            title="Wybierz folder"
        )
        if folder_path:
            # Tutaj przekażemy ścieżkę folderu do głównej aplikacji
            if hasattr(self, 'on_folder_selected'):
                self.on_folder_selected(folder_path)
        
    def save_file(self):
        # Przekaż żądanie zapisu do głównej aplikacji
        if hasattr(self, 'on_save_requested'):
            self.on_save_requested()
        
    def undo(self):
        pass
        
    def redo(self):
        pass
        
    def map_blocks(self):
        # Przekaż żądanie mapowania bloków do głównej aplikacji
        if hasattr(self, 'on_mapping_requested'):
            self.on_mapping_requested() 