from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    if env['CM_DATASET_PATH'] == "NIL":
        env['CM_DATASET_TRAIN_PATH'] = os.path.join(os.getcwd(),"train.csv")
        env['CM_DATASET_TEST_PATH'] = os.path.join(os.getcwd(),"test.csv")
        env['CM_DATASET_SOLUTION_PATH'] = os.path.join(os.getcwd(),"solution.csv")
    else:
        env['CM_DATASET_TRAIN_PATH'] = os.path.join(env['CM_DATASET_PATH'], "train.csv")
        env['CM_DATASET_TEST_PATH'] =os.path.join(env['CM_DATASET_PATH'], "test.csv")
        env['CM_DATASET_SOLUTION_PATH'] = os.path.join(env['CM_DATASET_PATH'], "solution.csv") 

    return {'return':0}
