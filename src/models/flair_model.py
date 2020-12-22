from model import *

#flair imports
from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus, ColumnCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings,DocumentLSTMEmbeddings, BertEmbeddings, StackedEmbeddings, TokenEmbeddings
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger
from typing import List
from flair.data import Sentence
import pandas as pd
import os
import re

class FlairModel(Model):
    """Class to train/test a model using flair.""" 
    def __init__(self, parameters):
        Model.__init__(self, model_format="bio_format", parameters=parameters)
        self.learning_rate= float(parameters['lr'])
        self.batch_size= int(parameters['batch'])
        self.mode=parameters['mode']
        
    def convert_format(self, dataset):
        filepath = "src/tmp/format.txt"
        if os.path.exists(filepath):
            os.remove(filepath)

        file = open(filepath, "w")
        pos_beg = 0
        pos_end = 1
        annot_beg = 0
        annot_end = 1
        label = None
        matches = None
        json_file = dataset.file

        for obj in json_file:
            pattern = re.compile(r"\w'|\w+|[^\w\s]")
            matches = pattern.finditer(obj['text'])

            if not matches:
                print("error")
                return

            for m in matches:
                file.write(m.group())
                file.write(" ")
                pos_beg = m.span()[0]
                pos_end = m.span()[1]

                for e in obj['entities']:
                    annot_beg = e[0]
                    annot_end = e[1]
                    label = e[2]

                    #At the beginning of the entity's position
                    if pos_beg == annot_beg:
                        file.write("B-"+label)
                        
                    #between the entity's position
                    elif pos_beg > annot_beg and pos_end <= annot_end:
                        file.write("I-"+label)
                    else:
                        file.write("O")

                file.write("\n")
            file.write("\n")

        file.close()
        return filepath

    def train(self):
        path = "./src/tmp/"
        self.training_data = self.convert_format(self.training_data)
    
        corpus: Corpus = ColumnCorpus(".", {0: 'text', 1: 'ner'},
                                    train_file=self.training_data
                                    )
        tag_dictionary = corpus.make_tag_dictionary(tag_type='ner')
        embedding_types: List[TokenEmbeddings] = [

            WordEmbeddings('fr'),
            FlairEmbeddings('fr-forward'),
            FlairEmbeddings('fr-backward'),
        ]

        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
        tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                                embeddings=embeddings,
                                                tag_dictionary=tag_dictionary,
                                                tag_type='ner',
                                                use_crf=True)
        self.trainer = ModelTrainer(tagger, corpus)
        save_path = path + self.model_name
        self.trainer.train(save_path,learning_rate=self.learning_rate,mini_batch_size=self.batch_size, max_epochs=self.nb_iter,embeddings_storage_mode=self.mode)
        self.is_ready = 1



    def test(self, test_data):
        path = "./src/tmp/"
        filepath = path + self.model_name + '/best-model.pt'
        data = self.convert_format(test_data)
        model = SequenceTagger.load(filepath)
        corpus: Corpus = ColumnCorpus(".", {0: 'text', 1: 'ner'},
                                        train_file=data,
                                        test_file=data
                                      )
        result, eval_loss = model.evaluate(corpus.test)
        results = result.detailed_results
        global_res = result.log_line
        global_res = global_res.split("\t")
        res={"model_name" : self.model_name}
        res["precision"] = float(global_res[0])*100
        res["recall"] = float(global_res[1])*100
        res["f_score"] = float(global_res[2])*100
        results = results.split("\n")
        results = results[6:]
        score_by_labels = {}
        for scores in results:
            scores = scores.replace("/s"," ")
            scores = scores.split()
            score_by_labels[scores[0]] = {'p' : float(scores[11])*100, 'r' : float(scores[14])*100, 'f' : float(scores[17])*100}
        res["score_by_label"]  = score_by_labels
        loss_path = path + self.model_name + "/loss.tsv"
        df = pd.read_csv(loss_path, sep = "\t" )
        self.losses = df["TRAIN_LOSS"].tolist()
        return res