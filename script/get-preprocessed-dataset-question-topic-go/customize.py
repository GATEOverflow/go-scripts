import os

def preprocess(i):

    os_info = i['os_info']
    env = i['env']

    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_PREPROCESSED_DATASET_TRAIN_PATH'] = os.path.join(os.getcwd(),"Preprocessed_train.csv")
    env['CM_PREPROCESSED_DATASET_TEST_PATH'] = os.path.join(os.getcwd(),"Preprocessed_test.csv")
    env['CM_PREPROCESSED_DATASET_SOLN_PATH'] = os.path.join(os.getcwd(),"Preprocessed_soln.csv")

    print("  Preprocessed training dataset path:"+env['CM_PREPROCESSED_DATASET_TRAIN_PATH'])

    return {'return':0}
