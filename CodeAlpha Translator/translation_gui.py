# translation_gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from translation_logic import LanguageTranslatorApp, SORTED_LANGUAGES_GOOGLE
import threading
import pyperclip

class TranslatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Language Translator (CodeAlpha)")
        master.geometry("650x500") # Slightly more compact
        master.configure(bg="#f0f0f0")

        self.translator_app = LanguageTranslatorApp()
        self.languages = SORTED_LANGUAGES_GOOGLE
        self.language_names = list(self.languages.values())
        self.language_codes = list(self.languages.keys())

        tk.Label(master, text="Language Translator", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        lang_frame = tk.Frame(master, bg="#e0e0e0", pady=5)
        lang_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(lang_frame, text="From:", font=("Arial", 10), bg="#e0e0e0").grid(row=0, column=0, padx=5, pady=5)
        self.source_lang_var = tk.StringVar()
        self.source_lang_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang_var, 
                                              values=["Auto-Detect"] + self.language_names, width=18, state="readonly", font=("Arial", 9))
        self.source_lang_combo.current(0) 
        self.source_lang_combo.grid(row=0, column=1, padx=5, pady=5)

        self.swap_button = tk.Button(lang_frame, text="↔", font=("Arial", 10, "bold"), command=self.swap_languages, width=2)
        self.swap_button.grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(lang_frame, text="To:", font=("Arial", 10), bg="#e0e0e0").grid(row=0, column=3, padx=5, pady=5)
        self.target_lang_var = tk.StringVar()
        self.target_lang_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang_var, 
                                              values=self.language_names, width=18, state="readonly", font=("Arial", 9))
        try: self.target_lang_combo.current(self.language_names.index("english"))
        except ValueError: self.target_lang_combo.current(0)
        self.target_lang_combo.grid(row=0, column=4, padx=5, pady=5)
        
        lang_frame.grid_columnconfigure(1, weight=1)
        lang_frame.grid_columnconfigure(4, weight=1)

        input_area_frame = tk.Frame(master, bg="#f0f0f0")
        input_area_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(input_area_frame, text="Enter Text:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.input_text = scrolledtext.ScrolledText(input_area_frame, height=6, wrap=tk.WORD, font=("Arial", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        self.input_text.focus()

        input_btn_frame = tk.Frame(input_area_frame, bg="#f0f0f0")
        input_btn_frame.pack(fill=tk.X)
        tk.Button(input_btn_frame, text="Clear In", font=("Arial", 9), command=lambda: self.input_text.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=2)
        tk.Button(input_btn_frame, text="Copy In", font=("Arial", 9), command=lambda: self.copy_to_clipboard(self.input_text.get("1.0", tk.END).strip())).pack(side=tk.LEFT, padx=2)


        self.translate_button = tk.Button(master, text="Translate", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=self.perform_translation_threaded)
        self.translate_button.pack(pady=5)

        output_area_frame = tk.Frame(master, bg="#f0f0f0")
        output_area_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(output_area_frame, text="Translation:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(output_area_frame, height=6, wrap=tk.WORD, font=("Arial", 10), state="disabled")
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0,5))

        output_btn_frame = tk.Frame(output_area_frame, bg="#f0f0f0")
        output_btn_frame.pack(fill=tk.X)
        tk.Button(output_btn_frame, text="Clear Out", font=("Arial", 9), command=self.clear_output).pack(side=tk.LEFT, padx=2)
        tk.Button(output_btn_frame, text="Copy Out", font=("Arial", 9), command=lambda: self.copy_to_clipboard(self.output_text.get("1.0", tk.END).strip())).pack(side=tk.LEFT, padx=2)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def copy_to_clipboard(self, text):
        if not text or text == "Translating...":
            self.status_var.set("Nothing to copy.")
            return
        try:
            pyperclip.copy(text)
            self.status_var.set("Text copied to clipboard.")
        except Exception as e:
            self.status_var.set("Clipboard error.")
            messagebox.showerror("Clipboard Error", "Could not copy. Ensure pyperclip is installed and functional (e.g., xclip/xsel on Linux).")
            
    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

    def swap_languages(self):
        src_name = self.source_lang_var.get()
        tgt_name = self.target_lang_var.get()
        if src_name == "Auto-Detect":
            self.status_var.set("Cannot swap 'Auto-Detect'. Select a specific source language.")
            return
        self.source_lang_var.set(tgt_name)
        self.target_lang_var.set(src_name)
        self.status_var.set("Languages swapped.")
        # Optionally swap text content as well
        in_text = self.input_text.get("1.0", tk.END).strip()
        out_text = self.output_text.get("1.0", tk.END).strip()
        if out_text and out_text != "Translating...":
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", out_text)
            self.clear_output() # Clear output as input changed

    def perform_translation_threaded(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text: return

        src_name = self.source_lang_var.get()
        tgt_name = self.target_lang_var.get()
        src_code = "auto" if src_name == "Auto-Detect" else self.language_codes[self.language_names.index(src_name)]
        tgt_code = self.language_codes[self.language_names.index(tgt_name)]

        self.translate_button.config(state=tk.DISABLED)
        self.status_var.set("Translating...")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "Translating...")
        self.output_text.config(state="disabled")

        threading.Thread(target=self._execute_translation, args=(text, tgt_code, src_code), daemon=True).start()

    def _execute_translation(self, text, target_code, source_code):
        translated = self.translator_app.translate_text(text, target_code, source_code)
        
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", translated)
        self.output_text.config(state="disabled")
        
        self.translate_button.config(state=tk.NORMAL)
        self.status_var.set("Translation complete." if "Error:" not in translated else "Translation failed.")

if __name__ == '__main__':
    try:
        import pyperclip
    except ImportError:
        print("Warning: pyperclip module not found. Copy to clipboard will not work. Install with 'pip install pyperclip'")
    root = tk.Tk()
    gui = TranslatorGUI(root)
    root.mainloop()