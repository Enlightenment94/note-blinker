import tkinter as tk
from tkinter import ttk
from chat.gpt import GPTAPI
import os
from tkinter import messagebox

class ChatPanel:
    def __init__(self, parent, editor):
        self.frame = ttk.LabelFrame(parent, text="Czat")
        self.frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Zapisz referencję do edytora
        self.editor = editor
        
        # Konfiguracja rozmiarów
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Inicjalizacja API GPT
        try:
            self.gpt = GPTAPI()
        except Exception as e:
            tk.messagebox.showerror("Błąd", f"Nie udało się zainicjalizować API GPT: {str(e)}")
            self.gpt = None
            
        # Inicjalizacja zmiennych
        self.mapped_blocks = []
        self.current_block_index = None
        self.last_response = None
        
        # Dodaj przyciski do nagłówka
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Przyciski Mapuj bloki i Prompt
        ttk.Button(header_frame, text="Mapuj bloki", command=self.map_blocks).pack(side=tk.LEFT, padx=5)
        ttk.Button(header_frame, text="Prompt", command=self.show_prompt).pack(side=tk.LEFT, padx=5)
        ttk.Button(header_frame, text="Chat", command=self.show_chat).pack(side=tk.LEFT, padx=5)
        
        self.setup_chat()
        
    def setup_chat(self):
        # Panel wyświetlania wiadomości
        self.chat_display = tk.Text(self.frame, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Panel bloków
        self.blocks_frame = ttk.Frame(self.frame)
        self.blocks_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Panel wprowadzania wiadomości
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Zmiana Entry na Text dla wprowadzania wiadomości
        self.chat_input = tk.Text(input_frame, height=20)  # Zwiększona wysokość
        self.chat_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Button(input_frame, text="Wyślij", command=self.send_message).pack(side=tk.RIGHT, padx=5)
        
    def map_blocks(self):
        """Wywołuje funkcję mapowania bloków z głównej aplikacji"""
        if hasattr(self, 'on_map_blocks'):
            self.on_map_blocks()
            
    def show_prompt(self):
        """Wyświetla aktualny prompt"""
        if self.current_block_index is not None:
            self.select_block(self.current_block_index)
            
    def show_chat(self):
        """Wyświetla tylko odpowiedź chata"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        
        # Znajdź najnowszy plik w folderze chat-story
        chat_story_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chat-story')
        if os.path.exists(chat_story_dir):
            chat_files = [f for f in os.listdir(chat_story_dir) if f.startswith('chat_') and f.endswith('.txt')]
            if chat_files:
                latest_file = max(chat_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
                latest_file_path = os.path.join(chat_story_dir, latest_file)
                with open(latest_file_path, 'r', encoding='utf-8') as f:
                    response = f.read()
                    self.chat_display.insert(tk.END, response)
        
        self.chat_display.config(state=tk.DISABLED)
        
    def display_blocks(self, blocks):
        # Wyczyść panel bloków
        for widget in self.blocks_frame.winfo_children():
            widget.destroy()
            
        self.mapped_blocks = blocks
        
        # Dodaj przyciski dla każdego bloku
        for i, block in enumerate(blocks):
            btn = ttk.Button(self.blocks_frame, text=f"Blok {i+1}", 
                           command=lambda idx=i: self.select_block(idx))
            btn.pack(side=tk.LEFT, padx=2)
            
        # Dodaj przycisk New obok przycisków bloków
        ttk.Button(self.blocks_frame, text="New", command=self.add_new_block).pack(side=tk.LEFT, padx=2)
            
    def select_block(self, index):
        """Wywołuje mapowanie bloków przed wyborem bloku"""
        # Najpierw zmapuj bloki, aby mieć aktualną wersję tekstu
        self.map_blocks()
        
        # Następnie wybierz blok
        self.current_block_index = index
        
        try:
            # Odczytaj prompt z pliku
            prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chat', 'prompt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt = f.read()
                
            # Pobierz bloki od wybranego do tyłu jako context
            context_blocks = self.mapped_blocks[:index]
            # Wybrany blok jako currenttext
            current_block = self.mapped_blocks[index]
            
            # Dodaj bloki jako context
            if context_blocks:
                context_text = "\n".join(block.split('>', 1)[1].rsplit('<', 1)[0].strip() for block in context_blocks)
                prompt += f"\nKontekst:\n{{-+{context_text}-+}}\n\n"
            
            # Dodaj wybrany blok jako currenttext
            current_text = current_block.split('>', 1)[1].rsplit('<', 1)[0].strip()
            prompt += f"Aktualny blok do edycji:\n{{-+{current_text}-+}}\n\n"
            
            # Dodaj pole na polecenia użytkownika z aktualną zawartością inputa
            user_prompt = self.chat_input.get('1.0', tk.END).strip()
            prompt += f"Polecenie:\n{{-+{user_prompt}-+}}\n"
            
            # Wyświetl prompt w panelu czatu
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.insert(tk.END, prompt)
            self.chat_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaktualizować promptu: {str(e)}")
        
    def send_message(self):
        if not self.gpt:
            messagebox.showerror("Błąd", "API GPT nie jest dostępne")
            return
            
        if self.current_block_index is None:
            messagebox.showerror("Błąd", "Najpierw wybierz blok do edycji")
            return
            
        try:
            # Odczytaj prompt z pliku
            prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chat', 'prompt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt = f.read()
                
            # Pobierz bloki od wybranego do tyłu jako context
            context_blocks = self.mapped_blocks[:self.current_block_index]
            # Wybrany blok jako currenttext
            current_block = self.mapped_blocks[self.current_block_index]
            
            # Dodaj bloki jako context
            if context_blocks:
                context_text = "\n".join(block.split('>', 1)[1].rsplit('<', 1)[0].strip() for block in context_blocks)
                prompt += f"\nKontekst:\n{{-+{context_text}-+}}\n\n"
            
            # Dodaj wybrany blok jako currenttext
            current_text = current_block.split('>', 1)[1].rsplit('<', 1)[0].strip()
            prompt += f"Aktualny blok do edycji:\n{{-+{current_text}-+}}\n\n"
            
            # Dodaj pole na polecenia użytkownika z aktualną zawartością inputa
            user_prompt = self.chat_input.get('1.0', tk.END).strip()
            prompt += f"Polecenie:\n{{-+{user_prompt}-+}}\n"
            
            # Wyślij prompt do GPT i wyświetl odpowiedź
            response = self.gpt.send_message(prompt)
            self.last_response = response  # Zapisz odpowiedź
            
            # Zapisz odpowiedź do pliku w folderze chat-story
            chat_story_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chat-story')
            os.makedirs(chat_story_dir, exist_ok=True)
            
            # Znajdź najnowszy plik w folderze chat-story
            chat_files = [f for f in os.listdir(chat_story_dir) if f.startswith('chat_') and f.endswith('.txt')]
            if chat_files:
                latest_file = max(chat_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
                latest_num = int(latest_file.split('_')[1].split('.')[0])
                new_num = latest_num + 1
            else:
                new_num = 1
                
            # Zapisz nową odpowiedź
            chat_file = os.path.join(chat_story_dir, f'chat_{new_num}.txt')
            with open(chat_file, 'w', encoding='utf-8') as f:
                f.write(response)
            
            # Wyświetl odpowiedź w panelu czatu
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.insert(tk.END, response)
            self.chat_display.config(state=tk.DISABLED)
            
            # Dodaj przycisk Accept
            accept_frame = ttk.Frame(self.frame)
            accept_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Button(accept_frame, text="Accept", command=self.accept_changes).pack(side=tk.RIGHT, padx=5)
            
            # Wyczyść pole wprowadzania
            self.chat_input.delete('1.0', tk.END)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wysłać wiadomości: {str(e)}")
            
    def accept_changes(self):
        """Zastępuje wybrany blok odpowiedzią z chata"""
        if self.current_block_index is None or not self.last_response:
            messagebox.showerror("Błąd", "Nie ma odpowiedzi do zaakceptowania")
            return
            
        try:
            # Zapisz indeks aktualnego bloku
            current_index = self.current_block_index
            
            # Pobierz zawartość edytora
            content = self.editor.editor.get('1.0', tk.END)
            
            # Podziel na bloki
            blocks = content.split('\n\n')
            
            # Zastąp wybrany blok odpowiedzią
            blocks[current_index] = self.last_response
            
            # Połącz bloki z powrotem
            new_content = '\n\n'.join(blocks)
            
            # Zastąp całą zawartość edytora
            self.editor.editor.delete('1.0', tk.END)
            self.editor.editor.insert('1.0', new_content)
            
            # Odśwież mapowanie bloków
            self.map_blocks()
            
            # Wybierz ten sam blok
            self.current_block_index = current_index
            self.select_block(current_index)
            
            # Wyczyść odpowiedź
            self.last_response = None
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaakceptować zmian: {str(e)}")
            
    def add_new_block(self):
        """Dodaje nowy blok tekstu"""
        try:
            # Pobierz zawartość edytora
            content = self.editor.editor.get('1.0', tk.END)
            
            # Dodaj nowy blok na końcu
            new_content = content.rstrip() + '\n\n>Nowy blok<'
            
            # Zastąp zawartość edytora
            self.editor.editor.delete('1.0', tk.END)
            self.editor.editor.insert('1.0', new_content)
            
            # Odśwież mapowanie bloków
            self.map_blocks()
            
            # Wybierz nowy blok
            if self.mapped_blocks:
                self.current_block_index = len(self.mapped_blocks) - 1
                self.select_block(self.current_block_index)
                
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się dodać nowego bloku: {str(e)}")
            
    def grid(self, **kwargs):
        self.frame.grid(**kwargs) 