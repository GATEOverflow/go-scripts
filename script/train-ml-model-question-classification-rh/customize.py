from cmind import utils
import os
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  

#training phase of LinearSVC model as we have seen earlier that it work best
def rohan_text_classificattion_training(train_Q,train_label, tfidf_vect):
    X_train_tfidf = tfidf_vect.fit_transform(train_Q)
    # model=LinearSVC(penalty='l2',C=2.8).fit(tfidf_vect.transform(train_Q),train_label)
    base_svc=SVC(C=8)
    model = CalibratedClassifierCV(base_svc).fit(tfidf_vect.transform(train_Q),train_label)
    return model

def create_model_rohan(train_Q, train_label):
    #tfidf initialization
    tfidf_vect = TfidfVectorizer(min_df=2,norm='l2',ngram_range=(1,2),stop_words='english',sublinear_tf=True,encoding='latin-1')
    #model creation 
    model = rohan_text_classificattion_training(train_Q, train_label, tfidf_vect)
    return model, tfidf_vect

def preprocess(i):

    os_info = i['os_info']

    env = i['env']
    trainfile = get_data_file(env['CM_PREPROCESSED_DATASET_TRAIN_PATH'])
    model, tfidf_vect = create_model_rohan(trainfile['Question'], trainfile['Tag'])
    pickle.dump(tfidf_vect, open("tfidf_obj", 'wb'))
    pickle.dump(model, open("model_rh.sav", 'wb'))
    print("model created!")

    return {'return':0}


def postprocess(i):
    env = i['env']
    env['CM_ML_MODEL'] = os.path.join(os.getcwd(),"model_rh.sav")
    env['CM_DATASET_TRAINED_MODEL_TFIDQ'] = os.path.join(os.getcwd(),"tfidf_obj")
    print("Trained model path is:"+env['CM_ML_MODEL'])

    return {'return':0}
