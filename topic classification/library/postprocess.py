from .preprocess import *

#function to get the correctness value
def nofequaltones(dsol):
  tag = []
  for i in dsol['Tag']:
    tag.append(i)
  return tag



def predict_rohan(model, tfidf_vect, test_Q):
    #predicting test data
    p=model.predict(tfidf_vect.transform(preprocess_text(test_Q)))
    return p