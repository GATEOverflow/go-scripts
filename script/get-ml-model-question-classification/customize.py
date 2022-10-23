from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    print(env['CM_DATASET_TRAINED_MODEL'])
    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_DATASET_SELECTED_MODEL_#1'] = os.path.join(os.getcwd(),"topicclassfication_#1.sav")
    return {'return':0}
