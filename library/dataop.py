import pandas as pd


#combining the training data files
def combine(data1, data2): #not needed
  combine_data=data1.append(data2,ignore_index=True)
  return combine_data['Question'],combine_data['Tag']

#rename specific column
def rename_column(datafile, init, final):
  datafile = datafile.rename(columns={init:final})
  return datafile

#get the input data to train the model
def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  

#get the specific column for processing
def get_data_train(data, tag):      #tag is the name of the column to be extracted
    return data[tag]