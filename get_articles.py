#!/home/eleonore/virtenvs/nltk-gensim-skl/bin/python2.7
# -*- coding: utf-8 -*-
import os, sys, time, json, codecs
from os import listdir, mkdir
from os.path import isfile, join
from bs4 import BeautifulSoup

## Let's parse xml articles from eLifeScience:

## 1) Use beautiful soup to get the subject, first auth, id
## 2) Add metadata to ARTICLES: {"subject": [{article, subgroup, name, year}]}
## 3) Create a directory with the "subject" name and copy the cleaned content
## to a text file named: id.txt

ARTICLES = {}

spe_char = {u'\u2013': '-', u'\xb1': "plus-minus"}

def debug_unicode(text):
    #print "Opening article with BS..."
    soup = BeautifulSoup(open(text), ["lxml", "xml"])
    #print "Getting the abstract content..."
    abstract_block = soup.find_all("abstract")
    print len(abstract_block)
    for abstract in abstract_block:
        if abstract:
            abstract_text = abstract.p.text
            print abstract_text
            print "*" * 30
    # counter = 0
    # try:
    #     for char in abstract_text:
    #         counter += 1
    #         pass
    # except UnicodeEncodeError:
    #     print "Error after character ", counter
    #     print char
    # return counter

def sort_articles(path="../elife-articles/"):
    # Get all xml files from path
    path_files = [f for f in listdir(path) if isfile(join(path,f))] or []
    xml_files = filter(lambda x: '.xml' in x, path_files)
    if len(xml_files) > 0:
        print "Total number of articles: %d" % len(xml_files)
        counter, errors = 0, 0
        for article in xml_files:
            # For each xml file add info to the ARTICLES dictionary
            try:
                soup = BeautifulSoup(open(path+article), ["lxml", "xml"])
                journal_id = soup.find("journal-id").string
                pub_id = soup.find("article-id").string
                subjects = soup.find_all("subj-group")
                auth_sn = soup.find("surname").string
                auth_fn = soup.find("given-names").string
                if len(subjects) == 2:
                    counter += 1
                    unique_subj = subjects[1].string
                    if not unique_subj in ARTICLES.keys():
                        ARTICLES[unique_subj] = [{"file": article, "journal_id": journal_id,
                                                  "pub_id": pub_id,
                                                  "first_auth": "%s, %s" %(auth_sn, auth_fn)}]
                    else:
                        ARTICLES[unique_subj].append({"file": article, "journal_id": journal_id,
                                                      "pub_id": pub_id,
                                                      "first_auth": "%s, %s" %(auth_sn, auth_fn)})
            except:
                errors += 1
                pass
        print "There are %d articles out of %s with a single subject." % (counter, len(xml_files))
        print "There is/are %d exception(s). \n" % errors

def store_articles_json(filename, articles_dict):
    with open(filename, 'w') as f:
        json.dump(articles_dict, f)

def read_articles_json(filename):
    with open(filename, 'r') as f:
        articles = json.load(f)
        return articles

# Get xml files for a particular category:
def get_xml_category(category, json_articles):
    # Get info for a category and create a list:
    cat = json_articles.get(category)
    xml_category = [f.get("file") for f in cat]
    return xml_category

# Write txt files for each xml in a category:
def write_txt_category(category, list_category, in_path="../elife-articles/", out_path="./articles/"):
    "Go throught the list and use BS to get text content."
    for article in list_category:
        print in_path+article
        article_text = ""
        soup = BeautifulSoup(open(in_path+article), ["lxml", "xml"])
        abstract_tag = soup.find_all("abstract")
        body_tag = soup.find_all("body")
        for b in body_tag[0]:
            try:
                article_text += " " + b.p.text
            except:
                for i in b:
                    try:
                        article_text += " " + i.p.text
                    except:
                        article_text += " " + i.string
        if abstract_tag:
            for abstract in abstract_tag:
                abstract_text = abstract.p.text
                article_text += "\n" + abstract_text

        for a in article_text:
            if a in spe_char.keys():
                final_article = article_text.replace(a, unicode(spe_char.get(a)))

        if not category in listdir(out_path):
            mkdir(out_path+category)
            print category, " folder created!"
        file_path = out_path + category + "/" + article.replace("xml", "txt")
        # Write to a text file:
        with codecs.open(file_path, mode='w', encoding='utf-8') as f:
            f.write(final_article)
    print "Wrote %d xml articles to text format." % len(list_category[:1])


if __name__ == "__main__":
    startTime = time.time()
    
    ## Sort articles
    #sort_articles()
    #print "%d categories in the dictionary" % len(ARTICLES.keys())
    #for i in ARTICLES.keys():
        #print "%d articles in the category %s" % (len(ARTICLES.get(i)), i)
    ## Store the dictionnary
    #store_articles_json("articles.json", ARTICLES)

    ## List the xml files for a category
    art_dict = read_articles_json("articles.json")
    #list_xml = get_xml_category("Neuroscience", art_dict)
    #write_txt_category("Neuroscience", list_xml)
    list_xml2 = get_xml_category("Cell biology", art_dict)
    write_txt_category("Cell biology", list_xml2)

    #debug_unicode("../elife-articles/elife03005.xml")
    print "\n"
    elapsedTime = time.time() - startTime
    print "This script took %f seconds to run" % elapsedTime
    
    
        
