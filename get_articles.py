#!/home/eleonore/virtenvs/nltk-gensim-skl/bin/python2.7
# -*- coding: utf-8 -*-
import os, sys
from os import listdir
from os.path import isfile, join

ARTICLES ={}

def sort_articles(path=os.chdir("../elife-articles/" )):
    path_files = [f for f in listdir(path) if isfile(join(path,f))] or []
    xml_files = filter(lambda x: '.xml' in x, path_files)
    if len(xml_files) > 0:
        for article in xml_files:
            ## 1) Use beautiful soup to get the <subj-group subj-group-type="heading"><subject>,
            ## the <subj-group subj-group-type="heading"><subject>, the first
            ## <contrib contrib-type="author"><name> and
            ## <pub-date date-type="pub" publication-format="electronic"><year>
            ## 2) Add metadata to ARTICLES: {"subject": [article, subgroup, name, year]}
            ## 3) Create a directory with the "subject" name and copy the cleaned content
            ## named: subgoup_year_name
            pass



if __name__ == "__main__":
    pass
        
