from cmind import utils
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

#get the input data to train the model
def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  


def preprocess(i):

    os_info = i['os_info']
    
    env = i['env']

    testfile = get_data_file(env['CM_PREPROCESSED_DATASET_TEST_PATH'])
    loaded_model = pickle.load(open(env['CM_ML_MODEL'], 'rb'))
    p=loaded_model.predict(env['CM_DATASET_TRAINED_MODEL_TFIDQ'].transform(testfile['Question']))
    testfile['Tag'] = p
    print(testfile)
    testfile.to_csv('Predicted_answers.csv')
    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_ML_MODEL_ANSWER'] = os.path.join(os.getcwd(),"Predicted_answers.csv")
    return {'return':0}
