from .preprocess import *
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

#training phase of LinearSVC model as we have seen earlier that it work best
def rohan_text_classificattion_training(train_Q,train_label, tfidf_vect):
    X_train_tfidf = tfidf_vect.fit_transform(train_Q)
    model=LinearSVC(penalty='l2',C=2.8).fit(tfidf_vect.transform(preprocess_text(train_Q)),train_label)
    return model

def create_model_rohan(train_Q, train_label):
    #tfidf initialization
    tfidf_vect = TfidfVectorizer(min_df=2,norm='l2',ngram_range=(1,2),stop_words='english',sublinear_tf=True,encoding='latin-1')
    #model creation 
    model = rohan_text_classificattion_training(train_Q, train_label, tfidf_vect)
    return model, tfidf_vect