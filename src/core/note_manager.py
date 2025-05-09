import json
import os
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.notes = {}
        self.notes_file = "notes.json"
        self.load_notes()
        
    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as f:
                    self.notes = json.load(f)
            except:
                self.notes = {}
        else:
            self.notes = {}
            
    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f)
            
    def create_note(self, title, content="", parent=None):
        note_id = str(datetime.now().timestamp())
        self.notes[note_id] = {
            'title': title,
            'content': content,
            'parent': parent
        }
        self.save_notes()
        return note_id
        
    def create_folder(self, title, parent=None):
        folder_id = str(datetime.now().timestamp())
        self.notes[folder_id] = {
            'title': title,
            'content': '',
            'parent': parent,
            'is_folder': True
        }
        self.save_notes()
        return folder_id
        
    def delete_item(self, item_id):
        if item_id in self.notes:
            del self.notes[item_id]
            self.save_notes()
            
    def get_note(self, note_id):
        return self.notes.get(note_id)
        
    def update_note(self, note_id, title=None, content=None):
        if note_id in self.notes:
            if title is not None:
                self.notes[note_id]['title'] = title
            if content is not None:
                self.notes[note_id]['content'] = content
            self.save_notes()
            
    def get_children(self, parent_id=None):
        return [note_id for note_id, note in self.notes.items() 
                if note.get('parent') == parent_id] 