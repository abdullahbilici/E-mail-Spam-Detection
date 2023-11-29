# E-Mail Spam Classification
# YZV 311E Term Project
#Abdullah Bilici, 150200330
#Bora Boyacıoğlu, 150200310

import numpy as np

import string
import spacy

from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter

from sklearn.metrics import classification_report, confusion_matrix

nlp = spacy.load('en_core_web_sm')
def tokenize_sentence(sentence):
    # Error handling for non-string inputs
    if not isinstance(sentence, str):
        return []
    
    # Tokenise the sentence
    tokenized = nlp(sentence)
    
    # Define stop words and punctuations in one set
    filter_lemma = STOP_WORDS | set(string.punctuation)
    
    tokens = []
    for token in tokenized:
        # Lowercase and lemmatise the words
        lemma = token.lemma_.lower().strip() if token.pos_ != "PRON" else token.lower_
        
        # Remove stop words and punctuations
        if lemma and lemma not in filter_lemma:
            tokens.append(lemma)
    
    return tokens


def term_frequency(documents):
    token_counts = list()
    for document in documents:
        # Error handling for non-list inputs
        if not document:
            token_counts.append({})
            continue
        document = document[1:]

        # Count the number of times each token appears in the document
        token_count = Counter(document).items()
        
        # Normalise the token count by the total number of tokens in the document
        total_tokens = len(document)
        token_count_normalized = {token: count/ total_tokens for token, count in token_count}
        
        token_counts.append(token_count_normalized)
    
    return token_counts


def inverse_document_frequency(documents):

    total_documents = len(documents)

    # Count the number of documents each token appears in
    token_counts = Counter()
    for document in documents:
        document = document[1:]

        token_counts.update(set(document))

    # Calculate the IDF score for each token
    idf_values = {term: np.log(total_documents / (count + 1)) + 1e-10 for term, count in token_counts.items() if count > 1} 
    return idf_values


def tfidf_calculator(tf, idf):

    scores = list()
    for document in tf:
        
        # Calculate the TF-IDF score for each token in the document
        document_score ={token: frequency * idf[token] for token, frequency in document.items() if token in idf}
        scores.append(document_score)

    return scores


def concatenate_loader(loader):
    Xs, ys = [], []
    for batch in loader:
        X, y = batch
        Xs.append(X)
        ys.append(y)
    return np.concatenate(Xs, axis=0), np.concatenate(ys, axis=0)

def evaluate_model(loader, model):
    all_preds = []
    all_true = []
    for batch in loader:
        X, y = batch

        # Ensure X is a 2D array
        if len(X.shape) == 1:
            X = X.reshape(1, -1)

        preds = model.predict(X)
        all_preds.extend(preds)
        all_true.extend(y)

    # Print the classification report and confusion matrix
    print(classification_report(all_true, all_preds))
    print(confusion_matrix(all_true, all_preds))
