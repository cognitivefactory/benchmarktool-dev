
from pathlib import Path
from dataset import *
import os
import csv
import pandas as pd

#spaCy imports
import spacy
from tqdm import tqdm
from spacy import displacy
from spacy.scorer import Scorer
import random
from spacy.gold import GoldParse


#flair imports
from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus, ColumnCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings,DocumentLSTMEmbeddings, BertEmbeddings, StackedEmbeddings, TokenEmbeddings
from flair.trainers import ModelTrainer
from flair.models import SequenceTagger
from typing import List
from flair.data import Sentence


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


class SpacyModel(Model):
    def __init__(self, parameters, model=None):
        Model.__init__(self,
                        model_format="spacy_format",
                        parameters=parameters)

        self.model = model
        self.visuals = []
    
    def get_visuals(self):
        return self.visuals 

    def convert_format(self, dataset):
        json_file=dataset.file
        data=[]
        for obj in json_file :
            entities = []
            for e in obj['entities'] :
                entities.append(tuple(e))
            data.append((obj['text'], {'entities' : entities}))
        return data

    def train(self):
        if self.model is not None:
            self.nlp = spacy.load(model)
            # print("Loaded model '%s'" % model)
        else:
            self.nlp = spacy.blank('fr')
            # print("Created new model")


        if 'ner' not in self.nlp.pipe_names:
            self.ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe(self.ner)
        else:
            self.ner = self.nlp.get_pipe('ner')
<<<<<<< HEAD
            

        if self.model is None:
=======
        labels = [ label for label in training_data.get_labels()]
        for l in labels :
            self.ner.add_label(l)
        if model is None:
>>>>>>> 2374ae270e77300565abdb16512d4000a9d376cd
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()

<<<<<<< HEAD
        labels = [ label for label in self.training_data.labels]
        for l in labels :
            self.ner.add_label(l)

        self.training_data = self.convert_format(self.training_data)
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        
        with self.nlp.disable_pipes(*other_pipes):
            training_loss = []
            for itn in range(self.nb_iter):
                random.shuffle(self.training_data)
                losses = {}
                
=======
    def get_visuals(self):
        return self.visuals 
            
    def train(self):
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        with self.nlp.disable_pipes(*other_pipes):
            for itn in range(self.nb_iter):
                random.shuffle(self.training_data)
                losses = {}
>>>>>>> 2374ae270e77300565abdb16512d4000a9d376cd
                for text, annotations in tqdm(self.training_data):
                    self.nlp.update([text], [annotations], sgd=self.optimizer, drop=0.35,
                        losses=losses)
                print(losses)
<<<<<<< HEAD
                training_loss.append(losses["ner"])
            print(training_loss)
        self.losses = training_loss
        self.is_ready = 1

                
    def test(self, test_data):
        data = self.convert_format(test_data)
        res={"model_name" : self.model_name}
        scorer = Scorer()
        for sents, ents in data:
=======
        self.is_ready = True
                
    def test(self, test_data):
        scorer = Scorer()
        for sents, ents in test_data:
>>>>>>> 2374ae270e77300565abdb16512d4000a9d376cd
            doc_gold = self.nlp.make_doc(sents)
            gold = GoldParse(doc_gold, entities=ents['entities'])
            pred_value = self.nlp(sents)
            visual = displacy.render(pred_value, style="ent")
            visual = visual.replace("\n\n","\n")
            self.visuals.append(visual)
            scorer.score(pred_value, gold)
<<<<<<< HEAD
            score = scorer.scores
        res["precision"] = score["ents_p"]
        res["recall"] = score["ents_r"]
        res["f_score"] = score["ents_f"]
        score["ents_per_type"]
        res["score_by_label"] = score["ents_per_type"]
        return res

    """save : not used for now
=======
        return scorer.scores
   

    def convert_format(self):
        json_file=self.training_data.get_file()
        data=[]
        for obj in json_file :
            entities = []
            for e in obj['entities'] :
                entities.append(tuple(e))
            data.append((obj['text'], {'entities' : entities}))
        self.training_data=data
        return data
    
>>>>>>> 2374ae270e77300565abdb16512d4000a9d376cd
    def save(self):
        if self.out_dir is not None:
            self.out_dir = Path(self.out_dir)
        if not self.out_dir.exists():
            self.out_dir.mkdir()
        self.nlp.to_disk(self.out_dir)
        print("Modele saved in :", self.out_dir)
<<<<<<< HEAD
    """


class FlairModel(Model):
    """Class to train/test a model using flair.""" 
    def __init__(self, parameters):
        Model.__init__(self, model_format="bio_format", parameters=parameters)
        self.model_name = parameters['model_name']
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
        filepath = "./src/tmp/" + self.model_name + "/best-model.pt"
        if not os.path.exists(filepath):
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
            save_path = "./src/tmp/" + self.model_name
            self.trainer.train(save_path,learning_rate=self.learning_rate,mini_batch_size=self.batch_size, max_epochs=self.nb_iter,embeddings_storage_mode=self.mode)
        self.is_ready = 1



    def test(self, test_data):
        filepath = "./src/tmp/" + self.model_name + '/best-model.pt'
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
        loss_path = "./src/tmp/" + self.model_name + "/loss.tsv"
        df = pd.read_csv(loss_path, sep = "\t" )
        self.losses = df["TRAIN_LOSS"].tolist()
        return res
        
=======

                
>>>>>>> 2374ae270e77300565abdb16512d4000a9d376cd
