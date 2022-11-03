import torch
from transformers import RobertaTokenizer
import numpy as np
import torch.nn as nn
from transformers import AutoModel
from torch.utils.data import random_split
from transformers import get_linear_schedule_with_warmup
import json
import csv
import pandas as pd
import sklearn
from sklearn.metrics import *
import warnings

def get_data(testfile, solfile):
    filename = 'train' + '.csv'
    with open(filename, 'r') as csvfile:
        lines = csvfile.readlines()
    train_x, train_y = [], []
    categories_train = set()
    for line in lines:
        train_x.append(' '.join(line.split(',')[:-1]))
        train_y.append(line.split(',')[-1][:-1].strip())
        categories_train.add(line.split(',')[-1][:-1].strip())
        
    train_x, train_y = train_x[1:], train_y[1:]
    
    filename = 'solution' + '.csv'
    with open(filename, 'r') as csvfile:
        lines = csvfile.readlines()
    test_x, test_y = [], []
    categories_test = set()
    for line in lines:
        test_x.append(' '.join(line.split(',')[:-1]))
        test_y.append(line.split(',')[-1][:-1].strip())
        categories_test.add(line.split(',')[-1][:-1].strip())
    
    test_x, test_y = test_x[1:], test_y[1:]
    cat_to_idx = {}
    classes = 0
    for cat in categories_train.union(categories_test):
        if cat != 'Tag':
            cat_to_idx[cat] = classes
            classes += 1
    for i in range(len(train_y)):
        train_y[i] = cat_to_idx[train_y[i]]
    for i in range(len(test_y)):
        test_y[i] = cat_to_idx[test_y[i]]
        
    return train_x, train_y, test_x, test_y, cat_to_idx, categories_train, categories_test, classes

def preprocess(x):
    """
    This methods performs data preprocessing - 
    removing stop words, lowercasing, removing redundant whitespaces
    """
    import spacy    
    nlp = spacy.load("en_core_web_sm")
    #nlp.Defaults.stop_words
    x_new = []
    for text in x:
        my_doc = nlp(text)
        # Create list of word tokens
        token_list = []
        for token in my_doc:
            token_list.append(token.text)

        from spacy.lang.en.stop_words import STOP_WORDS
        # Create list of word tokens after removing stopwords
        filtered_sentence = [] 
        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False:
                filtered_sentence.append(word) 

        text = " ".join(filtered_sentence)
        text = text.lower()
        text = text.replace('_', '')
        text = " ".join(text.split())
        x_new.append(text)
    return x_new


def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    trainfile = get_data(env['CM_PREPROCESSED_DATASET_TRAIN_PATH'],)
    model, tfidf_vect = create_model_rohan(trainfile['Question'], trainfile['Tag'])
    env['CM_DATASET_TRAINED_MODEL_TFIDQ'] = tfidf_vect
    pickle.dump(model, open("topicclassfication_#1.sav", 'wb'))
    print("model created!")

    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_DATASET_TRAINED_MODEL'] = os.path.join(os.getcwd(),"topicclassfication_#1.sav")
    print("Trained model path is:"+env['CM_DATASET_TRAINED_MODEL'])

    return {'return':0}
