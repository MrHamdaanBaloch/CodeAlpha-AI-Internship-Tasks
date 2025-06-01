import json
import os
import re 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_NLTK_AVAILABLE = False
lemmatizer = None
stop_words = set()
word_tokenize_func = None

try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords as nltk_stopwords
    from nltk.tokenize import word_tokenize as nltk_word_tokenize_original # Keep original import

    nltk.data.find('corpora/wordnet.zip')
    nltk.data.find('corpora/stopwords.zip')
    nltk.data.find('tokenizers/punkt.zip')
    nltk.sent_tokenize("Test.") 

    lemmatizer = WordNetLemmatizer()
    stop_words = set(nltk_stopwords.words('english'))
    word_tokenize_func = nltk_word_tokenize_original 
    _NLTK_AVAILABLE = True
    print("NLTK components loaded successfully.")
except LookupError as e:
    print(f"Warning: NLTK resource missing ({e}). NLP features will be basic.")
  
except ImportError:
    print("Warning: NLTK library not found. NLP features will be basic.")
   
except Exception as e_init:
    print(f"An unexpected error occurred during NLTK initialization: {e_init}")
    print("NLP features will be basic.")


class FAQChatbotRobust:
    def __init__(self, faq_file_path="faqs.json", similarity_threshold=0.25):
        self.faqs = self._load_faqs(faq_file_path)
        self.similarity_threshold = similarity_threshold
        
        if not self.faqs:
            print(f"Warning: Using hardcoded default FAQs as '{faq_file_path}' was not found/invalid.")
            self.faqs = [{"question": "Default question?", "answer": "Default answer. FAQ file missing."}]

        self.questions = [faq['question'] for faq in self.faqs]
        self.answers = {faq['question'].lower().strip(): faq['answer'] for faq in self.faqs}

        self.processed_questions = [self._preprocess_text(q) for q in self.questions]
        
        self.vectorizer = TfidfVectorizer()
        if self.processed_questions and any(self.processed_questions):
            try:
                self.question_vectors = self.vectorizer.fit_transform(self.processed_questions)
            except ValueError:
                print("Warning: Could not fit TF-IDF vectorizer. All processed questions might be empty.")
                self.question_vectors = None
        else:
            self.question_vectors = None
            print("Warning: No valid questions to vectorize.")

       
        self.greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "yo", "sup"]
        self.greeting_responses = [
            "Hello! I'm the AlphaProduct FAQ Bot. How can I help you today?",
            "Hi there! Ask me anything about AlphaProduct.",
            "Hey! What can I do for you regarding AlphaProduct?"
        ]
        

        self.fallback_response = "I'm sorry, I couldn't find an answer for that. Please try rephrasing or contact support at services@codealpha.tech."
        if not _NLTK_AVAILABLE:
            self.fallback_response += " (NLP features are currently limited)."

    def _load_faqs(self, filepath):
      
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and all('question' in item and 'answer' in item for item in data):
                        return data
                print(f"Warning: {filepath} format incorrect.")
                return []
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
                return []
        return []


    def _preprocess_text(self, text):
       
        text_lower = text.lower()
        if _NLTK_AVAILABLE and word_tokenize_func and lemmatizer: 
            tokens = word_tokenize_func(text_lower) 
            lemmas = [lemmatizer.lemmatize(token) for token in tokens 
                      if token.isalnum() and token not in stop_words]
            return " ".join(lemmas)
        else:
            words = re.findall(r'\b\w+\b', text_lower)
            return " ".join(words)

    def get_response(self, user_query):
   
        print(f"\nDEBUG: Received user_query: '{user_query}'") 
        user_query_cleaned = user_query.lower().strip()
        print(f"DEBUG: Cleaned query: '{user_query_cleaned}'") 

      
        if hasattr(self, 'greetings') and self.greetings:
            print(f"DEBUG: Checking against greetings: {self.greetings}") 
            for greeting_keyword in self.greetings:
                print(f"DEBUG: Comparing '{user_query_cleaned}' with '{greeting_keyword}'") 
                if user_query_cleaned == greeting_keyword:
                    print(f"DEBUG: Greeting match found for '{greeting_keyword}'!") 
                    return np.random.choice(self.greeting_responses)
        else:
            print("DEBUG: self.greetings not found or empty. Skipping greeting check.")
        
        print("DEBUG: No greeting match. Proceeding to FAQ matching.")
    


        if not self.faqs or self.question_vectors is None or self.question_vectors.shape[0] == 0:
            return "My knowledge base is currently unavailable or not processed."

        processed_query_for_tfidf = self._preprocess_text(user_query) 
        print(f"DEBUG: Processed query for TF-IDF: '{processed_query_for_tfidf}'") 
        
        if not processed_query_for_tfidf.strip(): 
            print("DEBUG: Processed query for TF-IDF is empty. Returning fallback.") 
            return self.fallback_response

        try:
            query_vector = self.vectorizer.transform([processed_query_for_tfidf])
        except ValueError: 
             print("DEBUG: Error: TF-IDF Vectorizer not fitted. Returning fallback.") 
             return self.fallback_response + " (Error in query processing)."
             
        similarities = cosine_similarity(query_vector, self.question_vectors)
        
        if similarities.size > 0:
            max_sim_idx = np.argmax(similarities)
            max_similarity_score = similarities[0, max_sim_idx]
            
            print(f"DEBUG: Best FAQ Match='{self.questions[max_sim_idx]}', Processed FAQ='{self.processed_questions[max_sim_idx]}', Similarity={max_similarity_score:.4f}")

            if max_similarity_score >= self.similarity_threshold:
                original_question_key = self.questions[max_sim_idx].lower().strip()
                return self.answers.get(original_question_key, self.fallback_response)
        
        print("DEBUG: No strong FAQ match found. Returning fallback.")
        return self.fallback_response