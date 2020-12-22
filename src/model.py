from dataset import Dataset, TrainData
import csv

class Model(object):
    def __init__(self, model_format, parameters):
        self.model_name = parameters['model_name']
        self.nb_iter = int(parameters['nb_iter'])
        self.training_data = None
        self.is_ready = 0
        self.model_format=model_format.lower()
        self.losses = None

    def add_training_data(self, training_data):
        self.training_data = training_data

    def write_data(self,scores,csv_file):
        fieldnames = ['model_name', 'precision', 'recall', 'f_score','score_by_label', 'losses']
        scores["losses"] = self.losses
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(scores)