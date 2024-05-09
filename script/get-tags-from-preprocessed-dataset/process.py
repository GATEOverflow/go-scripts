import pandas as pd
import json
import os

def get_data_file(filename):    
    dtrain=pd.read_csv(filename,header=0)
    return dtrain  

testfile = get_data_file(os.environ['CM_PREPROCESSED_DATASET_SOLN_PATH'])
uniqueTags = testfile["Tag"].unique().tolist()
json_file_path = "tagList.json"
# Store the unique tags in a JSON file with key "tags"
with open(json_file_path, 'w') as json_file:
    json.dump({"tags": uniqueTags}, json_file)
print(uniqueTags)