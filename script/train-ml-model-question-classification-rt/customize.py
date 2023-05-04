import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datasets import load_dataset
from setfit import SetFitModel, SetFitTrainer
from sentence_transformers.losses import CosineSimilarityLoss
import os

def get_dataset_remote():
    dataset = load_dataset("ANANDHU-SCT/TOPIC_CLASSIFICATION")
    return dataset

def create_trainer(base_model, train_dataset, eval_dataset):
    trainer = SetFitTrainer(
        model=base_model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss_class=CosineSimilarityLoss,
        metric="accuracy",
        batch_size=16,
        num_iterations=1, # The number of text pairs to generate for contrastive learning
        num_epochs=1, # The number of epochs to use for contrastive learning
        column_mapping={"Question": "text", "label": "label"} # Map dataset columns to text/label expected by trainer
    )
    return trainer
    
def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    
    dataset = get_dataset_remote()
    train_dataset = dataset["train"]
    eval_dataset = dataset["validation"]
    base_model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2", multitarget=True)
    trainer = create_trainer(base_model, train_dataset, eval_dataset)
    #trainer.train()
    # metrics = trainer.evaluate()
    # print(metrics)
    base_model._save_pretrained("qn_classification_setfitModel")

    return {'return':0}


def postprocess(i):

    env = i['env']
    env['CM_ML_MODEL'] = os.path.join(os.getcwd(),"qn_classification_setfitMode")
    print("Trained model path is:"+env['CM_ML_MODEL'])

    return {'return':0}
