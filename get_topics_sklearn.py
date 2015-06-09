#!/home/eleonore/virtenvs/scikitlearn/bin/python
# -*- coding: utf-8 -*-
import string, re, codecs
import numpy as np
import get_topics as gt
from sklearn.feature_extraction.text import CountVectorizer

# Get text documents
ARTICLES = ["articles/conrad2013_melanoma.txt"]
TEXTS = []

for article in ARTICLES:
    a = gt.parse_text(article)
    b = gt.get_tokens(a)
    TEXTS.extend(gt.lemmatize_tokens(b))

print TEXTS

# Initialize the "CountVectorizer" object
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 


# Fit the model using fit_transform
train_data = vectorizer.fit_transform(TEXTS)

# Convert to numpy arreay
train_data = train_data.toarray()


