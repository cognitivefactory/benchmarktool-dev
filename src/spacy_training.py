# coding: utf-8

""" spacy_training : train a model using spaCy """

from __future__ import unicode_literals, print_function
import plac #  wrapper over argparse
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar
from spacy import displacy

from spacy.gold import GoldParse
from spacy.scorer import Scorer

def convert_format(json_file):
    """Convert JSON file to the format required to train a model using spaCy"""
        data = []
        for obj in json_file :
            entities = []
            for e in obj['entities'] :
                entities.append(tuple(e))
                
            if entities :
                data.append((obj['text'], {'entities' : entities}))
        return data

class Spacy_Model:
    """Class to train/test a model using spaCy"""
    
    def __init__(self,model,model_name, training_file,labels,out_dir, nb_iter):
        self.model_name = model_name
        self.nb_iter = nb_iter
        self.training_file = training_file
        self.out_dir=out_dir
        if model is not None:
            self.nlp = spacy.load(model)
            print("Loaded model '%s'" % model)
        else:
            self.nlp = spacy.blank('fr')
            print("Created blank'fr' model")
            
        if 'ner' not in self.nlp.pipe_names:
            self.ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe(self.ner)
 
        else:
            self.ner = nlp.get_pipe('ner')
            
        for l in labels :
            self.ner.add_label(l)
        if model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()
      
            
    def train(self):
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        with self.nlp.disable_pipes(*other_pipes):  # only train NER
            for itn in range(self.nb_iter):
                random.shuffle(self.training_file)
                losses = {}
                for text, annotations in tqdm(self.training_file):
                    self.nlp.update([text], [annotations], sgd=self.optimizer, drop=0.35,
                        losses=losses)
                print(losses)
                
    def test(self, test_data):
        doc = self.nlp(test_data)
        displacy.render(doc, style="ent", jupyter="true")
        return doc

    def evaluate(self, examples):
        scorer = Scorer()
        for sents, ents in examples:
            doc_gold = self.nlp.make_doc(sents)
            gold = GoldParse(doc_gold, entities=ents['entities'])
            pred_value = self.nlp(sents)
            displacy.render(pred_value, style="ent", jupyter="true")
            scorer.score(pred_value, gold)
        return scorer.scores

"""
LABELS = [label[1] for label in train.get_labels()] 
TRAIN_DATA = convert_format(train.get_content())

#Parameters
model = None# None : to create a new model
model_name = "Animal" 
out_dir = None #where to save the model
nb_iter = 15 

params = (model, model_name,TRAIN_DATA, LABEL, out_dir, nb_iter)
model = Model(model, model_name,TRAIN_DATA, LABEL, out_dir, nb_iter)
model.train()
test = [("On dit qu\'un cheval est calme",{
            'entities': [(13, 19, 'ANIMAL')]
            }),
            ("Un cheval endormi n\'est pas nécessairement un zèbre calme",{
             'entities': [(3, 9, 'ANIMAL'),(46,51, 'ANIMAL')]   
            })
           ]
res = model.evaluate(test)

#ents_p = entities_precision
#ents_r = entities_recall
#ents_f = entities_f_score
print("precision : {}, recall : {}, f_score : {}".format(res['ents_p'],res['ents_r'], res['ents_f']))
"""