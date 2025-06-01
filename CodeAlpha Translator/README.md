# CodeAlpha AI Internship - Task 1: Language Translation Tool

## Description
A simple desktop application that translates text from one language to another using the `deep_translator` library (leveraging Google Translate). The GUI is built with Tkinter.

## Features
- Auto-detect source language or select manually.
- Select target language from a comprehensive list.
- Real-time translation (as you type, with debounce - *Basic implementation, manual button is primary*).
- Swap source and target languages.
- Copy input and output text to clipboard.
- Clear input and output text fields.
- Responsive GUI with status updates.

## Technologies Used
- Python 3.x
- Tkinter (for GUI)
- `deep_translator` library (for translation)
- `pyperclip` library (for clipboard functionality)
- `threading` (for non-blocking API calls)

## Setup and Installation
1.  **Prerequisites:**
    *   Python 3.6 or higher.
    *   Tkinter (usually included with Python).
    *   For clipboard functionality on Linux, you might need `xclip` or `xsel`:
        ```bash
        sudo apt-get install xclip 
        # or
        sudo apt-get install xsel
        ```
2.  **Clone the repository (or download files).**
3.  **Navigate to the project directory:**
    ```bash
    cd CodeAlpha_LanguageTranslator 
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run
Execute the GUI script from the project directory:
```bash
python translation_gui.py