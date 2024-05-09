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

    if(env['CM_ML_MODEL_NAME'] == "go_2"):
        dataset = load_dataset("ANANDHU-SCT/TOPIC_CLASSIFICATION")
        model = SetFitModel.from_pretrained(env['CM_ML_MODEL'])
        probs = model.predict_proba(dataset['test']['Question'])
        final_result = []
        resultfile = pd.DataFrame()
        resultfile["Question"] = dataset["test"]["Question"]
        resultfile["Tag"] = dataset["test"]["Tag"]
        resultfile["Actual soln"] = dataset["test"]["label"]
        for prob in probs:
            print(type(prob))
            try:
                topk_values, topk_indices = torch.topk(torch.from_numpy(prob), k=5)
            except:    
                topk_values, topk_indices = torch.topk(prob, k=5)
            # print(torch.argmax(prob, dim=0)
            final_result.append(topk_indices.tolist())
        resultfile["PredictedLabels"] = final_result
        resultfile.to_csv('Predicted_answers.csv')
        
        return {'return':0}
        # print(probs)
    elif(env['CM_ML_MODEL_NAME'] == "GPT3.5"):
        testfile = get_data_file(env['CM_DATASET_SOLUTION_PATH'])
        tagList = env["CM_DATASET_TAGS"]
        print(testfile.head(5))
        print(tagList)
        return {'return':0}
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
        testfile['PredictedLabels'] = solutions
        testfile['Probabilities'] = main_list

        testfile.to_csv('Predicted_answers.csv')

        return {'return':0}


def postprocess(i):
    env = i['env']
    env['CM_ML_MODEL_ANSWER'] = os.path.join(os.getcwd(),"Predicted_answers.csv")
    return {'return':0}
