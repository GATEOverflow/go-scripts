from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_DATASET_TRAIN_PATH'] = os.path.join(os.getcwd(),"train.csv")

    return {'return':0}
