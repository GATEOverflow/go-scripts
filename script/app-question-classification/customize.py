from cmind import utils
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import csv
import numpy as np
from setfit import SetFitModel
from datasets import load_dataset
import torch

def preprocess(i):

    os_info = i['os_info']
    
    env = i['env']

    return {'return':0}


def postprocess(i):
    env = i['env']
    env['CM_ML_MODEL_ANSWER'] = os.path.join(os.getcwd(),"Predicted_answers.csv")
    return {'return':0}
