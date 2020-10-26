
from pathlib import Path
from dataset import *
import os

#spaCy imports
import spacy
from tqdm import tqdm # loading bar
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

def convert_format(dataset, model_format):
        #spaCy
        if model_format == "spacy_format" :
            json_file=dataset.file
            data=[]
            for obj in json_file :
                entities = []
                for e in obj['entities'] :
                    entities.append(tuple(e))
                data.append((obj['text'], {'entities' : entities}))
            return data


        #flair
        elif model_format == "bio_format":
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
            json_file=dataset.file
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
        



class Model(object):
    def __init__(self, model_format, parameters):
        self.model_name = parameters['model_name']
        self.nb_iter = int(parameters['nb_iter'])
        self.training_data = None
        self.out_dir = parameters['out_dir']
        self.is_ready = False
        self.model_format=model_format.lower()

    def add_training_data(self, training_data):
        self.training_data = training_data

class SpacyModel(Model):
    def __init__(self, parameters, model=None):
        print("----------")
        Model.__init__(self,
                        model_format="spacy_format",
                        parameters=parameters)

        self.model = model;
        self.visuals = []

    def get_visuals(self):
        return self.visuals 
            
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
            

        if self.model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()

        labels = [ label for label in self.training_data.labels]
        for l in labels :
            self.ner.add_label(l)

        self.training_data = convert_format(dataset=self.training_data, model_format=self.model_format)
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        
        with self.nlp.disable_pipes(*other_pipes):
            for itn in range(self.nb_iter):
                random.shuffle(self.training_data)
                losses = {}
                for text, annotations in tqdm(self.training_data):
                    self.nlp.update([text], [annotations], sgd=self.optimizer, drop=0.35,
                        losses=losses)
                print(losses)
        self.is_ready = True
                
    def test(self, test_data):
        # convert data format
        data = convert_format(dataset=test_data, model_format=self.model_format)


        scorer = Scorer()
        for sents, ents in data:
            doc_gold = self.nlp.make_doc(sents)
            gold = GoldParse(doc_gold, entities=ents['entities'])
            pred_value = self.nlp(sents)
            visual = displacy.render(pred_value, style="ent")
            visual = visual.replace("\n\n","\n")
            self.visuals.append(visual)
            scorer.score(pred_value, gold)
            print(scorer.scores)
        return scorer.scores
   

    def save(self):
        if self.out_dir is not None:
            self.out_dir = Path(self.out_dir)
        if not self.out_dir.exists():
            self.out_dir.mkdir()
        self.nlp.to_disk(self.out_dir)
        print("Modele saved in :", self.out_dir)



class FlairModel(Model):
    """Class to train/test a model using flair."""

    
    def __init__(self, parameters):
        Model.__init__(self, model_format="bio_format", parameters=parameters)
        self.model_name = './'+ parameters['model_name']
        self.learning_rate= float(parameters['lr'])
        self.batch_size= int(parameters['batch'])
        self.mode=parameters['mode']
        


    def train(self):
        self.training_data = convert_format(dataset=self.training_data, model_format=self.model_format)
       
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
        self.trainer.train(self.model_name,learning_rate=self.learning_rate,mini_batch_size=self.batch_size, max_epochs=self.nb_iter,embeddings_storage_mode=self.mode)
        self.is_ready = True



    def test(self, test_data):
        print(test_data)
        data = convert_format(dataset=test_data, model_format=self.model_format)

        model = SequenceTagger.load(self.model_name+'/best-model.pt')

        corpus: Corpus = ColumnCorpus(".", {0: 'text', 1: 'ner'},
                                        train_file=None,
                                        test_file=data
                                      )
        result, eval_loss = model.evaluate(corpus.test)
        # permet de retourner un dictionnaire de la même forme que celui fourni pas spaCy
        res = result.detailed_results
        res = res.replace("-", "").split()
        index_label = res.index('class:') + 1
        label = res[index_label]
        s = res[-6:]
        scores = {label : {'p': s[1], 'r': s[3], 'f': s[5]}}
        return scores
        

