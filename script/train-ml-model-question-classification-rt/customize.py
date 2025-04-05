import os

    
def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    
    return {'return':0}


def postprocess(i):

    env = i['env']
    env['MLC_ML_MODEL'] = os.path.join(os.getcwd(),"qn_classification_setfitModel")
    print("Trained model path is:"+env['MLC_ML_MODEL'])

    return {'return':0}
