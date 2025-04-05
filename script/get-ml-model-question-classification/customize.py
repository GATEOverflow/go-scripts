import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    print("get ml model:"+env['MLC_ML_MODEL'])  #MLC_ML_MODEL
    return {'return':0}


def postprocess(i):

    env = i['env']#MLC_ML_MODEL
    #env['MLC_DATASET_SELECTED_MODEL_#1'] = os.path.join(os.getcwd(),"topicclassfication_#1.sav")#deleteAc
    return {'return':0}
