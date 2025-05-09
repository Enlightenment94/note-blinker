# Note Blinker

A Python-based note-taking application with a graphical user interface built using Tkinter and AI-powered features.

## Description

Note Blinker is a desktop application that provides a modern interface for taking and managing notes. The application features a notebook-style interface with multiple tabs for organizing different notes, integrated AI chat capabilities, and a file management system.

## Features

- Modern GUI built with Tkinter
- Tab-based note organization
- Clean and intuitive user interface
- AI-powered chat integration
- File tree navigation
- Text editor with formatting capabilities
- Note management system
- Settings management

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- OpenAI (for AI chat features)
- python-dotenv (for environment variable management)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd note-blinker
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
note-blinker/
├── src/
│   ├── chat/
│   │   ├── gpt/
│   │   │   ├── api.py
│   │   │   └── __init__.py
│   │   ├── prompt
│   │   └── __init__.py
│   ├── core/
│   │   ├── file_operations.py
│   │   └── note_manager.py
│   ├── gui/
│   │   ├── components/
│   │   │   ├── chat_panel.py
│   │   │   ├── file_tree.py
│   │   │   ├── navbar.py
│   │   │   └── text_editor.py
│   │   └── app.py
│   ├── utils/
│   │   └── settings.py
│   └── main.py
├── mynote/
├── requirements.txt
└── README.md
```

## Running the Application

To start the application, run:
```bash
python src/main.py
```

## Development

The project is organized into several modules:

### GUI Components (`src/gui/`)
- `app.py`: Main application window and initialization
- `components/`: 
  - `chat_panel.py`: AI chat interface
  - `file_tree.py`: File navigation system
  - `navbar.py`: Navigation bar component
  - `text_editor.py`: Text editing interface

### Core Functionality (`src/core/`)
- `file_operations.py`: File handling and management
- `note_manager.py`: Note organization and management

### Chat Features (`src/chat/`)
- `gpt/api.py`: OpenAI API integration
- `prompt`: Chat prompt templates

### Utilities (`src/utils/`)
- `settings.py`: Application settings and configuration