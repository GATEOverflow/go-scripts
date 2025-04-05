import os
import pandas as pd
from sklearn.metrics import f1_score, precision_score
import ast


def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):
    correct = 0
    env = i['env']
    if(env['MLC_ML_MODEL_NAME'] == "go_2"):
        model_soln=pd.read_csv(env['MLC_ML_MODEL_ANSWER'],header=0)["PredictedLabels"]
        soln=pd.read_csv(env['MLC_ML_MODEL_ANSWER'],header=0)["Actual soln"]
        for i in range(len(model_soln)):
            if(soln[i] in ast.literal_eval(model_soln[i])):
                correct = correct + 1
        print("\tAccuracy by brute force approach is:"+str(correct/len(model_soln)))
    elif(env['MLC_ML_MODEL_PLATFORM'] == "OPENAI" or env['MLC_ML_MODEL_PLATFORM'] == "CLAUDE"):
        modelSolnData=pd.read_csv(env['MLC_ML_MODEL_ANSWER'],header=0)
        accuracy = (modelSolnData['Tag'] == modelSolnData['predictedTags']).mean()
        print(f"Accuracy through {env['MLC_ML_MODEL_NAME']} is{accuracy}")
        print(f"NOTE: The solution file is present in path: {env['MLC_ML_MODEL_ANSWER']}")
    else:
        soln=pd.read_csv(env['MLC_DATASET_SOLUTION_PATH'],header=0)["Tag"]
        model_soln=pd.read_csv(env['MLC_ML_MODEL_ANSWER'],header=0)["PredictedLabels"]
        model_soln_single_tag = pd.read_csv(env['MLC_ML_MODEL_ANSWER'],header=0)["Tag"]
        for i in range(len(model_soln)):
            if(soln[i] in model_soln[i]):
                correct = correct + 1
        print("\tAccuracy by brute force approach is:"+str(correct/len(model_soln)))
        # print("\n\tAccuracy of the result produced by model #1:"+str(f1_score(model_soln_single_tag, soln, average='micro'))+"\n")
    return {'return':0}
