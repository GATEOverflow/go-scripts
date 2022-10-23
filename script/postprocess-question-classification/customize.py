from cmind import utils
import os
import pandas as pd
from sklearn.metrics import f1_score

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    soln=pd.read_csv(env['CM_DATASET_SOLUTION_PATH'],header=0)["Tag"]
    model_soln=pd.read_csv(env['CM_DATASET_OUTPUT_MODEL_ANSWER'],header=0)["Tag"]
    print("\n\tAccuracy of the result produced by model #1:"+str(f1_score(model_soln, soln, average='micro'))+"\n")
    return {'return':0}
