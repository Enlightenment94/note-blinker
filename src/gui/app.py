import tkinter as tk
from tkinter import ttk, messagebox
from .components.navbar import Navbar
from .components.file_tree import FileTree
from .components.text_editor import TextEditor
from .components.chat_panel import ChatPanel
from utils.settings import Settings
import os
import re

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notatnik")
        self.root.geometry("1200x800")
        
        # Inicjalizacja zmiennych
        self.current_file = None
        self.settings = Settings()
        
        # Inicjalizacja głównych komponentów
        self.setup_ui()
        
        # Automatyczne otwarcie ostatniego folderu
        self._open_last_folder()
        
    def _open_last_folder(self):
        last_folder = self.settings.get_last_folder()
        if last_folder and os.path.isdir(last_folder):
            self.handle_folder_selected(last_folder)
            
            # Rekurencyjne szukanie pierwszego pliku tekstowego
            def find_first_text_file(item):
                item_path = self.file_tree.tree.item(item)['values'][0]
                if os.path.isfile(item_path):
                    try:
                        # Spróbuj otworzyć plik jako tekstowy
                        with open(item_path, 'r', encoding='utf-8') as f:
                            f.read()
                        return item_path
                    except:
                        pass
                for child in self.file_tree.tree.get_children(item):
                    result = find_first_text_file(child)
                    if result:
                        return result
                return None
                
            # Znajdź pierwszy plik tekstowy w całym drzewie
            for item in self.file_tree.tree.get_children():
                first_file = find_first_text_file(item)
                if first_file:
                    self.handle_file_selected(first_file)
                    # Zmapuj bloki
                    self.handle_mapping_requested()
                    # Wybierz ostatni blok
                    if self.chat_panel.mapped_blocks:
                        self.chat_panel.current_block_index = len(self.chat_panel.mapped_blocks) - 1
                        self.chat_panel.select_block(self.chat_panel.current_block_index)
                    break
        
    def setup_ui(self):
        # Główny kontener
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Pasek nawigacyjny
        self.navbar = Navbar(self.main_container)
        self.navbar.on_folder_selected = self.handle_folder_selected
        self.navbar.on_save_requested = self.handle_save_requested
        
        # Obszar roboczy
        self.workspace = ttk.Frame(self.main_container)
        self.workspace.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Konfiguracja rozmiarów kolumn i wierszy
        self.workspace.columnconfigure(0, weight=1)  # Drzewo plików
        self.workspace.columnconfigure(1, weight=3)  # Edytor
        self.workspace.columnconfigure(2, weight=1)  # Czat
        self.workspace.rowconfigure(0, weight=1)     # Jeden wiersz zajmujący całą wysokość
        
        # Inicjalizacja komponentów
        self.file_tree = FileTree(self.workspace)
        self.file_tree.on_file_selected = self.handle_file_selected
        
        self.text_editor = TextEditor(self.workspace)
        self.chat_panel = ChatPanel(self.workspace, self.text_editor)
        
        # Połącz funkcję mapowania bloków
        self.chat_panel.on_map_blocks = self.handle_mapping_requested
        
    def handle_folder_selected(self, folder_path):
        # Zapisz ścieżkę folderu
        self.settings.set_last_folder(folder_path)
        
        # Czyszczenie istniejącego drzewa
        for item in self.file_tree.tree.get_children():
            self.file_tree.tree.delete(item)
            
        # Dodawanie głównego folderu
        root_item = self.file_tree.tree.insert("", "end", text=os.path.basename(folder_path), 
                                             values=(folder_path,), open=True)
        
        # Rekurencyjne dodawanie zawartości folderu
        self._add_folder_contents(root_item, folder_path)
        
    def _add_folder_contents(self, parent_item, folder_path):
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    # Dodawanie folderu
                    folder_item = self.file_tree.tree.insert(parent_item, "end", text=item,
                                                           values=(item_path,))
                    self._add_folder_contents(folder_item, item_path)
                else:
                    # Dodawanie pliku
                    self.file_tree.tree.insert(parent_item, "end", text=item,
                                             values=(item_path,))
        except PermissionError:
            # Pomijanie folderów bez uprawnień
            pass
            
    def handle_file_selected(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_editor.set_content(content)
                self.current_file = file_path
        except UnicodeDecodeError:
            # Jeśli plik nie jest tekstowy, wyświetl komunikat
            self.text_editor.set_content("Nie można wyświetlić zawartości pliku - nie jest to plik tekstowy.")
            self.current_file = None
        except Exception as e:
            self.text_editor.set_content(f"Błąd podczas otwierania pliku: {str(e)}")
            self.current_file = None
            
    def handle_save_requested(self):
        if self.current_file:
            try:
                content = self.text_editor.get_content()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {str(e)}")
        else:
            messagebox.showwarning("Uwaga", "Nie wybrano pliku do zapisania")
            
    def handle_mapping_requested(self):
        if not self.current_file:
            messagebox.showwarning("Uwaga", "Nie wybrano pliku do mapowania")
            return
            
        try:
            content = self.text_editor.get_content()
            mapped_blocks = self._map_blocks(content)
            
            # Wyświetl zmapowane bloki w panelu czatu
            self.chat_panel.display_blocks(mapped_blocks)
            
            # Wyświetl zmapowane bloki w czacie
            self.chat_panel.chat_display.config(state=tk.NORMAL)
            self.chat_panel.chat_display.delete('1.0', tk.END)
            self.chat_panel.chat_display.insert(tk.END, "Zmapowane bloki XML:\n\n")
            for block in mapped_blocks:
                self.chat_panel.chat_display.insert(tk.END, f"{block}\n\n")
            self.chat_panel.chat_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zmapować bloków: {str(e)}")
            
    def _map_blocks(self, content):
        # Podziel tekst na bloki (oddzielone pustymi liniami)
        blocks = []
        current_block = []
        block_number = 1
        
        for line in content.split('\n'):
            if line.strip():  # Jeśli linia nie jest pusta
                current_block.append(line)
            elif current_block:  # Jeśli mamy zebrany blok i trafiliśmy na pustą linię
                block_text = '\n'.join(current_block)
                tag = f"note_{block_number}"
                blocks.append(f"<{tag}>\n{block_text}\n</{tag}>")
                current_block = []
                block_number += 1
                
        # Dodaj ostatni blok jeśli istnieje
        if current_block:
            block_text = '\n'.join(current_block)
            tag = f"note_{block_number}"
            blocks.append(f"<{tag}>\n{block_text}\n</{tag}>")
                
        return blocks 

    def setup_navigation(self):
        """Konfiguracja paska nawigacyjnego"""
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Przyciski nawigacyjne
        ttk.Button(nav_frame, text="Nowy", command=self.new_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Otwórz", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Zapisz", command=self.save_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Zapisz jako", command=self.save_file_as).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Prompt", command=self.handle_prompt_requested).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Chat", command=self.handle_chat_requested).pack(side=tk.LEFT, padx=5) 