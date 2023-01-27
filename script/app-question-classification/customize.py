from cmind import utils
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import csv
import numpy as np

#get the input data to train the model
def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  

def get_trainfile_solnval(filename):
    testfile = get_data_file(filename)
    l = []
    data = testfile['Tag']
    for value in data:
        if value not in l:
            l.append(value)
    return l

def preprocess(i):

    os_info = i['os_info']
    
    env = i['env']
    print(env['CM_ML_MODEL_NAME'])
    if(env['CM_ML_MODEL_NAME'] == "go_3"):
        print("GOT INTO THE SETFIT MODEL SPECIFIC CODE!")
        #load the test dataset
        from datasets import load_dataset
        from setfit import SetFitModel
        dataset = load_dataset("ANANDHU-SCT/TOPIC_CLASSIFICATION")
        #get the trained model
        model = SetFitModel.from_pretrained(env['CM_ML_MODEL'])
        p = model.predict(dataset['test']['Question'])
        print(len(p))
        prob = model.predict_proba(dataset['test']['Question'])
        testfile = get_data_file(env['CM_PREPROCESSED_DATASET_TEST_PATH'])
        print(testfile)
        ans_list = get_trainfile_solnval(env['CM_PREPROCESSED_DATASET_TRAIN_PATH'])
        soln_file = get_data_file(env['CM_DATASET_SOLUTION_PATH'])["Tag"]
    else:
        testfile = get_data_file(env['CM_PREPROCESSED_DATASET_TEST_PATH'])
        ans_list = get_trainfile_solnval(env['CM_PREPROCESSED_DATASET_TRAIN_PATH'])
        soln_file = get_data_file(env['CM_DATASET_SOLUTION_PATH'])["Tag"]

        loaded_model = pickle.load(open(env['CM_ML_MODEL'], 'rb'))
        tfidfvect = pickle.load(open(env['CM_DATASET_TRAINED_MODEL_TFIDQ'], 'rb'))

        p=loaded_model.predict(tfidfvect.transform(testfile['Question']))
        prob=loaded_model.predict_proba(tfidfvect.transform(testfile['Question']))

    main_list=[]
    sub_list=[]
    solutions = []
    sub_solutions = []
    print(len(testfile))
    for ques_prob in prob:
        for probs in ques_prob:
            if probs>0.02:
                sub_list.append(probs)
                index = np.where(ques_prob==probs)[0].tolist()[0]
                sub_solutions.append(ans_list[index])
        main_list.append(sub_list)
        solutions.append(sub_solutions)
        sub_list=[]
        sub_solutions=[]

    testfile['Tag'] = p
    testfile['Actual soln'] = soln_file
    testfile['List_of_ans'] = solutions
    testfile['Probabilities'] = main_list

    testfile.to_csv('Predicted_answers.csv')
    
    return {'return':0}


def postprocess(i):
    env = i['env']
    env['CM_ML_MODEL_ANSWER'] = os.path.join(os.getcwd(),"Predicted_answers.csv")
    return {'return':0}


#TO-DO
#save the train and test dataset from the setfit hub and integrate with other modules.