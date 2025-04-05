import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    if 'MLC_SETFIT_DATASET' not in env:
        env['MLC_SETFIT_DATASET'] = "ANANDHU-SCT/TOPIC_CLASSIFICATION"
    if 'MLC_DATASET_PATH' not in env:
        env['MLC_DATASET_TRAIN_PATH'] = os.path.join(os.getcwd(),"train.csv")
        env['MLC_DATASET_TEST_PATH'] = os.path.join(os.getcwd(),"test.csv")
        env['MLC_DATASET_SOLUTION_PATH'] = os.path.join(os.getcwd(),"solution.csv")
    else:
        env['MLC_DATASET_TRAIN_PATH'] = os.path.join(env['MLC_DATASET_PATH'], "train.csv")
        env['MLC_DATASET_TEST_PATH'] =os.path.join(env['MLC_DATASET_PATH'], "test.csv")
        env['MLC_DATASET_SOLUTION_PATH'] = os.path.join(env['MLC_DATASET_PATH'], "solution.csv") 

    return {'return':0}
