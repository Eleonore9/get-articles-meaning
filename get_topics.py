#!/home/eleonore/virtenvs/nltk-gensim-skl/bin/python2.7
# -*- coding: utf-8 -*-
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import models
from gensim.corpora import Dictionary
from os import listdir
from os.path import isfile, join
import string, re, codecs, time


## Global variables
stop_words = ['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'but', 'for',
              'from', 'has', 'he', 'if', 'in', 'is', 'it', 'its', 'it\'s', 'not',
              'of', 'on', 'than', 'that', 'the', 'therefore', 'to', 'was',
              'were', 'will', 'with']

extra_sw = ['may', 'need', 'have', 'been', 'their', 'this', 'these', 'which', 'do', 'did']

spe_char = {u'β': 'beta', u'α': 'alpha', u'\u03bcm': 'mu', u'\xb5m': 'micron'}

## Functions to break up the process:
def parse_text(text_file):
    "Gets a text file outputs a list of strings."
    with codecs.open(text_file, mode='r', encoding='utf-8') as f:
        read = f.read()
        r = [read.replace(unicode(i), spe_char.get(i)) for i in read if i in spe_char.keys()] or [read]
        text = [line for line in r[0].strip().split('. ') if line != '']
        return text
    
def get_tokens(text_parsed):
    "Gets a text and retrieves tokens."
    # Tokenisation
    texts = [t.lower().replace('\n', ' ').split(' ') for t in text_parsed]
    # Remove punctuation and stop words
    tokens = [[filter(lambda x:x not in string.punctuation, i)
               for i in txt if i != '' and i not in stop_words] for txt in texts]
    tokens = [[filter(lambda x:x not in extra_sw, i)
               for i in txt if len(i) > 2 and not i.isdigit()] for txt in tokens]
    return tokens

def lemmatize_tokens(tokens):
    "Gets tokens and retrieves lemmatised tokens."
    # Lemmatisation using nltk lemmatiser
    lmtzr = WordNetLemmatizer()
    lemma = [[lmtzr.lemmatize(word) for word in data] for data in tokens]
    return lemma

def bag_of_words(lemma):
    "Takes in lemmatised words and returns a bow."
    ## Create bag of words from dictionnary
    dictionary = Dictionary(lemma)
    dictionary.save('text.dict')
    ## Term frequency–inverse document frequency (TF-IDF)
    bow = [dictionary.doc2bow(l) for l in lemma] # Calculates inverse document counts for all terms
    return bow

def tfidf_and_lsi(lemma, bow):
    "Gets a bow and returns topics."
    dictionary = Dictionary(lemma)
    tfidf = models.TfidfModel(bow) # Transforms the count representation into the Tfidf space
    corpus_tfidf = tfidf[bow]
    ## Build the LSI model
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=6)
    corpus_lsi = lsi[corpus_tfidf]
    list_topics = [] 
    for i in range(lsi.num_topics):
        print lsi.show_topic(i)
        list_topics.extend(lsi.show_topic(i))
    topics = [i[1] for i in list_topics]
    return topics

## Function to retrieve topics using nltk
def get_topics(text_file):
    txt = parse_text(text_file)
    tokens = get_tokens(txt)
    #print tokens
    lemma = lemmatize_tokens(tokens)
    bow = bag_of_words(lemma)
    return tfidf_and_lsi(lemma, bow)

## Get all text articles from a path and retrieve topics:
def list_all_articles(path):
    articles = [f for f in listdir(path) if isfile(join(path, f))] or []
    print "There are %d articles in %s" % (len(articles), path)
    return {"path": path, "articles": articles}

def get_articles_topics(list_articles):
    pass

if __name__ == "__main__":
    startTime = time.time()
    
    #print get_topics("zen.txt")
    #print get_topics('articles/conrad2013_melanoma.txt')
    #p = parse_text('articles/conrad2013_melanoma.txt')
    #print get_tokens(p)

    neuro_articles = list_all_articles("articles/Neuroscience/")
    cellbiol_articles = list_all_articles("articles/Cell biology/")
    #print get_tokens(parse_text(neuro_articles.get("path") + neuro_articles.get("articles")[0]))
    print get_topics(neuro_articles.get("path") + neuro_articles.get("articles")[0])

    print "\n"
    elapsedTime = time.time() - startTime
    print "This script took %f seconds to run" % elapsedTime

    
