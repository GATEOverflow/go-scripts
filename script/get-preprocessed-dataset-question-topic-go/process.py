from doctest import testfile
import os
import pandas as pd
import re
from tqdm import tqdm

#functions for data preprocessing
#rename specific column
def rename_column(datafile, init, final):
  datafile = datafile.rename(columns={init:final})
  return datafile

#get the input data to train the model
def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  

#save the excel file after modification
def savefile(file, filename):
    file.to_csv('Preprocessed_'+filename+'.csv')


#pre processing units
# https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
    #"functions", "relational", "safe", "variables", "regards", "languages", "statements", "true", "powerfull", "given", "following", "write", "without", "additional", "used", "obtain", "none",
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


# Combining all the above stundents 
def preprocess_text(text_data):
    preprocessed_text = []
    # tqdm is for printing the status bar
    for sentance in tqdm(text_data):
        sent = decontracted(sentance)
        sent = sent.replace('\\r', ' ')
        sent = sent.replace('\\n', ' ')
        sent = sent.replace('\\"', ' ')
        sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
        # https://gist.github.com/sebleier/554280
        sent = ' '.join(e for e in sent.split() if e.lower() not in stopwords)
        preprocessed_text.append(sent.lower().strip())
    return preprocessed_text



#preprocessing the training file
trainfile = get_data_file(os.environ['CM_DATASET_TRAIN_PATH'])
trainfile = rename_column(trainfile, ' Tag', 'Tag')
print(trainfile['Tag'].value_counts(ascending=True))  
trainfile['Question'] = preprocess_text(trainfile['Question'])
savefile(trainfile, "train")
print("File saved\n\n")
    
#for preprocessing the test file
testfile = get_data_file(os.environ['CM_DATASET_TEST_PATH'])
testfile['Question'] = preprocess_text(testfile['Question'])  
savefile(testfile, "test")
print("File saved\n\n")
#preprocessing the solution file
solnfile = get_data_file(os.environ['CM_DATASET_SOLUTION_PATH'])  
solnfile = rename_column(solnfile, ' Tag', 'Tag')
savefile(solnfile, "soln")
print("File saved\n\n")

