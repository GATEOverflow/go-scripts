import pandas as pd
import numpy as np
import imblearn
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer
import os

def get_dataset():
    #to load the dataset from setfit hub
    dataset = load_dataset("ANANDHU-SCT/TOPIC_CLASSIFICATION")
    print(dataset)
    train_dataset = dataset["train"]
    eval_dataset = dataset["validation"]
    return train_dataset, eval_dataset

def create_trainer(model, train_dataset, eval_dataset):
    # Create trainer
    trainer = SetFitTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss_class=CosineSimilarityLoss,
        metric="accuracy",
        batch_size=16,
        num_iterations=20, # The number of text pairs to generate for contrastive learning(20 was the given val)
        num_epochs=1, # The number of epochs to use for contrastive learning
        column_mapping={"Question": "text", "label": "label"} # Map dataset columns to text/label expected by trainer
    )
    return trainer

def train(trainer, model):
    # Train and evaluate
    trainer.train()
    model._save_pretrained("qn_classification")

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    #to assign the train and aval datasets
    train_dataset, eval_dataset = get_dataset()
    

    # Load a SetFit model from Hub
    model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")

    #create a trainer object
    trainer = create_trainer(model, train_dataset, eval_dataset)

    #to train the model
    train(trainer, model)

    metrics = trainer.evaluate()

    print("model created!")

    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_ML_MODEL'] = os.path.join(os.getcwd(),"qn_classification")
    print("Trained model path is:"+env['CM_ML_MODEL'])

    return {'return':0}
