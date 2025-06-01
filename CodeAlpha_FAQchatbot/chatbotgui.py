
import tkinter as tk
from tkinter import scrolledtext, END 
from chatbotlogic import FAQChatbotRobust, _NLTK_AVAILABLE 
import datetime
import threading

class FAQChatbotGUIRobust:
    def __init__(self, master):
        print("DEBUG: FAQChatbotGUIRobust __init__ started") 
        self.master = master
        master.title("FAQ Bot (CodeAlpha - Robust)")
        master.geometry("450x500")
        master.configure(bg="#f0f0f0")

        self.chatbot = None 
        self.default_faq_file = "faqs.json"

        tk.Label(master, text="AlphaProduct FAQ Bot", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        self.chat_history = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', height=15, font=("Arial", 9))
        self.chat_history.pack(pady=5, padx=10, expand=True, fill=tk.BOTH)

        self.status_label = tk.Label(master, text="Initializing...", font=("Arial", 8, "italic"), bg="#f0f0f0")
        self.status_label.pack(pady=2, padx=10, anchor='w')

        input_frame = tk.Frame(master, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.input_field = tk.Entry(input_frame, font=("Arial", 10), relief=tk.SOLID)
        self.input_field.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=4, padx=(0,5))
        self.input_field.bind("<Return>", self.send_message_event)

        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message, font=("Arial", 9, "bold"))
        self.send_button.pack(side=tk.RIGHT)
        
        self.configure_tags()
        print("DEBUG: Scheduling initialize_chatbot_threaded")
        self.master.after(100, self.initialize_chatbot_threaded)
        print("DEBUG: FAQChatbotGUIRobust __init__ finished") 


    def initialize_chatbot_threaded(self):
        print("DEBUG: initialize_chatbot_threaded started") 
        self.send_button.config(state=tk.DISABLED)
        self.input_field.config(state=tk.DISABLED)
        threading.Thread(target=self.initialize_chatbot, daemon=True).start()

    def initialize_chatbot(self):
        print("DEBUG: initialize_chatbot (in thread) started") 
        try:
            self.chatbot = FAQChatbotRobust(faq_file_path=self.default_faq_file)
            
            if not _NLTK_AVAILABLE: 
                self.add_to_chat_history("System", "NLTK advanced features disabled. Using basic text processing.")
                self.status_label.config(text="Bot ready (basic NLP).")
            elif self.chatbot.faqs and self.chatbot.question_vectors is not None:
                self.status_label.config(text="Bot ready (NLTK active).")
            else:
                self.status_label.config(text="Error: Chatbot knowledge base failed.")
                self.add_to_chat_history("System", "Error initializing knowledge base.")
            
            self.add_to_chat_history("Bot", "Hello! How can I help with AlphaProduct?")
        except Exception as e:
            print(f"ERROR in initialize_chatbot: {e}") 
            self.status_label.config(text="FATAL ERROR during chatbot init. Check console.")
            self.add_to_chat_history("System", f"ERROR during init: {e}")


        self.send_button.config(state=tk.NORMAL)
        self.input_field.config(state=tk.NORMAL)
        self.input_field.focus_set()
        print("DEBUG: initialize_chatbot (in thread) finished") 


    def configure_tags(self):
    
        self.chat_history.tag_config("You", font=("Arial", 9, "bold"), foreground="blue")
        self.chat_history.tag_config("Bot", font=("Arial", 9, "bold"), foreground="green")
        self.chat_history.tag_config("System", font=("Arial", 9, "bold"), foreground="orange red")
        self.chat_history.tag_config("text", font=("Arial", 9))
        self.chat_history.tag_config("time", font=("Arial", 7, "italic"), foreground="gray")

    def add_to_chat_history(self, sender, message):

        try:
            self.chat_history.config(state='normal')
            timestamp = datetime.datetime.now().strftime('%H:%M')
            self.chat_history.insert(tk.END, f"{sender} ", sender)
            self.chat_history.insert(tk.END, f"[{timestamp}]:\n", "time")
            self.chat_history.insert(tk.END, f"{message}\n\n", "text")
            self.chat_history.config(state='disabled')
            self.chat_history.yview(tk.END)
        except tk.TclError as e:
            print(f"Error adding to chat history (GUI likely not fully ready): {e}")


    def send_message_event(self, event): self.send_message()

    def send_message(self):
        
        user_input = self.input_field.get()
        if not user_input.strip():
            return
        if not self.chatbot: 
            self.add_to_chat_history("System", "Chatbot is not initialized properly.")
            return

        self.add_to_chat_history("You", user_input)
        self.input_field.delete(0, tk.END)
        
        self.send_button.config(state=tk.DISABLED)
        self.status_label.config(text="Bot thinking...")
        self.master.update_idletasks() 

        bot_response = self.chatbot.get_response(user_input)
        self.add_to_chat_history("Bot", bot_response)
        
        self.send_button.config(state=tk.NORMAL)
        self.status_label.config(text="Bot ready." + (" (basic NLP)" if not _NLTK_AVAILABLE else " (NLTK active)"))
        self.input_field.config(state=tk.NORMAL)
        self.input_field.focus_set()


if __name__ == '__main__':
    print("DEBUG: Script execution started (__main__)") 
    try:
        root = tk.Tk()
        print("DEBUG: tk.Tk() created") 
        gui = FAQChatbotGUIRobust(root)
        print("DEBUG: FAQChatbotGUIRobust instantiated") 
        root.mainloop()
        print("DEBUG: root.mainloop() finished") 
    except Exception as e:
        print("---------------------------------------------")
        print(f"FATAL ERROR in __main__: {e}") 
        import traceback
        traceback.print_exc() 
        print("---------------------------------------------")
        input("Press Enter to exit...") 