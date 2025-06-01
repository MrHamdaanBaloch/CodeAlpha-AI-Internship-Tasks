# CodeAlpha AI Internship - Task 2: FAQ Chatbot
## Description
A simple desktop chatbot that answers Frequently Asked Questions (FAQs) about "AlphaProduct". It uses NLTK for text processing and TF-IDF with Cosine Similarity for matching user queries to a knowledge base stored in `faqs.json`.

## Features
-   Loads FAQs from `faqs.json`.
-   Basic NLP: tokenization, lemmatization, stopword removal.
-   TF-IDF and Cosine Similarity for question matching.
-   Simple Tkinter GUI for interaction.

## Technologies Used
-   Python 3.x
-   Tkinter
-   NLTK
-   Scikit-learn

## Setup and Installation
1.  **Prerequisites:**
    *   Python 3.6 or higher.
2.  **Clone/Download:** Get project files.
3.  **Navigate to directory:** `cd CodeAlpha_FAQChatbot`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **NLTK Resources:**
    Ensure NLTK resources (`wordnet`, `stopwords`, `punkt`) are downloaded. If not, run Python and execute:
    ```python
    import nltk
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('punkt')
    ```
6.  **Knowledge Base:**
    The `faqs.json` file in this directory contains the Q&A pairs.

## How to Run
```bash
python faq_chatbot_gui_simple.py