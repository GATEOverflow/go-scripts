from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    print("get ml model:"+env['CM_ML_MODEL'])  #CM_ML_MODEL
    return {'return':0}


def postprocess(i):

    env = i['env']#CM_ML_MODEL
    #env['CM_DATASET_SELECTED_MODEL_#1'] = os.path.join(os.getcwd(),"topicclassfication_#1.sav")#deleteAc
    return {'return':0}
