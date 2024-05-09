from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']
    
    env = i['env']

    return {'return':0}


def postprocess(i):
    env = i['env']
    # env['CM_ML_MODEL_ANSWER'] = os.path.join(os.getcwd(),"Predicted_answers.csv")
    return {'return':0}
