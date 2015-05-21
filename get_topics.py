#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.stem.wordnet import WordNetLemmatizer
from gensim import models
from gensim.corpora import Dictionary
import string

## Global variables
stop_words = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
              'from', 'has', 'he', 'if', 'in', 'is', 'it', 'its', 'it\'s',
              'of', 'on', 'than', 'that', 'the', 'to', 'was', 'were', 'will', 'with']

## Function to parse the text
def parse_text(text_file):
    with open(text_file, 'r') as f:
        text = [line for line in f.read().split('\n') if line != '']
        return text
    
## Function to retrieve topics using nltk
def get_topics(input_text):
    '''Gets a text and retrieves topics'''
    # Tokenisation
    texts = [t.lower().replace('\n', ' ').split(' ') for t in input_text]
    # Remove punctuation and stop words
    docs = [[filter(lambda x:x not in string.punctuation, i)
             for i in txt if i != '' and i not in stop_words] 
            for txt in texts]
    # Lemmatisation
    lmtzr = WordNetLemmatizer()
    lemm = [[lmtzr.lemmatize(word) for word in data] for data in docs]
    ## Create bag of words from dictionnary
    dictionary = Dictionary(lemm)
    dictionary.save('text.dict')
    ## Term frequency–inverse document frequency (TF-IDF)
    bow = [dictionary.doc2bow(l) for l in lemm] # Calculates inverse document counts for all terms
    tfidf = models.TfidfModel(bow)              # Transforms the count representation into the Tfidf space
    corpus_tfidf = tfidf[bow]
    ## Build the LSI model
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
    corpus_lsi = lsi[corpus_tfidf]
    list_topics = [] 
    for i in range(lsi.num_topics):
        list_topics.extend(lsi.show_topic(i))
    topics = [i[1] for i in list_topics]
    return topics


if __name__ == "__main__":
    t = parse_text("zen.txt")
    print get_topics(t)
    
