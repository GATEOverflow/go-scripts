from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    if 'CM_SETFIT_DATASET' not in env:
        env['CM_SETFIT_DATASET'] = "ANANDHU-SCT/TOPIC_CLASSIFICATION"
    if 'CM_DATASET_PATH' not in env:
        env['CM_DATASET_TRAIN_PATH'] = os.path.join(os.getcwd(),"train.csv")
        env['CM_DATASET_TEST_PATH'] = os.path.join(os.getcwd(),"test.csv")
        env['CM_DATASET_SOLUTION_PATH'] = os.path.join(os.getcwd(),"solution.csv")
    else:
        env['CM_DATASET_TRAIN_PATH'] = os.path.join(env['CM_DATASET_PATH'], "train.csv")
        env['CM_DATASET_TEST_PATH'] =os.path.join(env['CM_DATASET_PATH'], "test.csv")
        env['CM_DATASET_SOLUTION_PATH'] = os.path.join(env['CM_DATASET_PATH'], "solution.csv") 

    return {'return':0}
