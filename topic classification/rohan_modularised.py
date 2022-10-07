from sklearn.metrics import f1_score

#from preprocess import *
from library.dataop import *
from library.topic_classification_training import *
from library.postprocess import *

#storing the questions and tags in a seperate variable
testfile = get_data_file('datasets/test.csv')
testfile_Q = get_data_train(testfile, 'Question')
solutionfile = get_data_file('datasets/solution.csv')
solutionfile = rename_column(solutionfile, ' Tag', 'Tag')
solutionfile_Q = get_data_train(solutionfile, 'Question')
solutionfile_A = get_data_train(solutionfile, 'Tag')
trainfile = get_data_file('datasets/train.csv')
trainfile = rename_column(trainfile, ' Tag', 'Tag')
trainfile_Q = get_data_train(trainfile, 'Question')
trainfile_A = get_data_train(trainfile, 'Tag')

#creating the model given by rohan
model, tfidf_vect = create_model_rohan(trainfile_Q, trainfile_A)

#predicting the question tags
p = predict_rohan(model, tfidf_vect, testfile_Q)
print(p)

correct_label = nofequaltones(solutionfile)
print(correct_label)

print(f1_score(p, correct_label, average='micro'))
"""
test_Q=get_data_train(dtest, 'Question')
model, tfidf_vect = create_model_rohan()
p = predict_rohan(model, tfidf_vect, test_Q)
print(p)
#f1_score using pred_labels and 2nd argument is correct_label that you need to provide.
correct_label = nofequaltones('.')
print(correct_label)
print(f1_score(p, correct_label, average='micro'))
"""