import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import csv
import numpy as np

from datasets import load_dataset

import json
from tqdm import tqdm

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

#get the openAI client object
def getOpenAIClient(APIKEY):
    from openai import OpenAI
    client = OpenAI(api_key=APIKEY)
    return client

#get the response form OpenAI
def getOpenAIresponse(openAIClient, content):
    response = openAIClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": content}
        ],
        temperature=0.2,
        top_p=0.1
    )
    formattedResponse = response.choices[0].message.content
    return formattedResponse


if(os.environ['CM_ML_MODEL_NAME'] == "go_2"):
    from setfit import SetFitModel
    import torch
    dataset = load_dataset("ANANDHU-SCT/TOPIC_CLASSIFICATION")
    model = SetFitModel.from_pretrained(os.environ['CM_ML_MODEL'])
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

    # print(probs)
elif(os.environ['CM_ML_MODEL_NAME'] == "GPT3.5"):
    testfile = get_data_file(os.environ['CM_DATASET_SOLUTION_PATH'])
    tagListPath = os.environ["CM_DATASET_TAGS"]
    tagListPath=r"{}".format(tagListPath)
    print(tagListPath)
    openAIClient = getOpenAIClient(os.environ["OPENAI_API_KEY"])
    with open(tagListPath, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    # Obtain the value of the key
    tagList = None
    for key in data:
        tagList = data[key]
    predictedTagList = []
    for question in tqdm(testfile['Question']):
        fewShotPrompt = f"""
        You are an expert topic classifier. Your role is to analyse a question and classify the question into any of the following question Tags:
        {tagList}
        The steps to infer the answer would be:
        1. Analyse the question    
        2. Infer the topic to which the question belongs.
        3. Check if the question belongs to any of the specific area within the infered topic. eg; if the topic to which the question belongs is arrays and on further analysis, if the question can be specifically associated with subtopic such as array multipliers (which comes within the topic array), then the topic to be asssigned to the question is array multiplier.
        4. If any specific subtopic is found , return that as answer else return the topic as the answer.
        5. return only the answer as string , dont explain.

        Here are some examples:

        input: The expression large frac x y x y 2 is equal to The maximum of x and y The minimum of x and y 1 None of the above 
        output: Absolute Value

        input: The number of full and half adders required to add 16 bit numbers is 8 half adders 8 full adders 1 half adder 15 full adders 16 half adders 0 full adders 4 half adders 12 full adders  
        output: Adder

        input: Suppose a fair six sided die is rolled once If the value on the die is 1 2 or 3 the die is rolled a second time What is the probability that the sum total of values that turn up is at least 6 dfrac 10 21 dfrac 5 12 dfrac 2 3 dfrac 1 6 
        output: Bayers Theorem

        input: {question}
        output:
        """
        response = getOpenAIresponse(openAIClient, fewShotPrompt)
        predictedTagList.append(response)
    testfile['predictedTags'] = predictedTagList
    testfile.to_csv(os.path.join(os.getcwd(),'Predicted_answers.csv'))
else:
    testfile = get_data_file(os.environ['CM_PREPROCESSED_DATASET_TEST_PATH'])
    ans_list = get_trainfile_solnval(os.environ['CM_PREPROCESSED_DATASET_TRAIN_PATH'])
    soln_file = get_data_file(os.environ['CM_DATASET_SOLUTION_PATH'])["Tag"]
    loaded_model = pickle.load(open(os.environ['CM_ML_MODEL'], 'rb'))
    tfidfvect = pickle.load(open(os.environ['CM_DATASET_TRAINED_MODEL_TFIDQ'], 'rb'))
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