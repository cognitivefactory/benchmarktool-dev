from pathlib import Path
import spacy
from tqdm import tqdm # loading bar
from spacy import displacy
from spacy.scorer import Scorer
import random
from spacy.gold import GoldParse

class Model(object):
    def __init__(self,model_name, training_data, nb_iter, out_dir):
        self.model_name = model_name
        self.nb_iter = nb_iter
        self.training_data = training_data
        self.out_dir = out_dir
        self.is_ready = False






class SpacyModel(Model):
    def __init__(self, model_name, training_data, nb_iter, out_dir,model):
        Model.__init__(self,model_name, training_data, nb_iter, out_dir)
        self.visuals = []
        if model is not None:
            self.nlp = spacy.load(model)
            print("Loaded model '%s'" % model)
        else:
            self.nlp = spacy.blank('fr')
            print("Created new model")
            
        if 'ner' not in self.nlp.pipe_names:
            self.ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe(self.ner)
        else:
            self.ner = self.nlp.get_pipe('ner')
        labels = [ label for label in training_data.get_labels()]
        for l in labels :
            self.ner.add_label(l)
        if model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()

    def get_visuals(self):
        return self.visuals 
            
    def train(self):
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
        scorer = Scorer()
        for sents, ents in test_data:
            doc_gold = self.nlp.make_doc(sents)
            gold = GoldParse(doc_gold, entities=ents['entities'])
            pred_value = self.nlp(sents)
            visual = displacy.render(pred_value, style="ent")
            visual = visual.replace("\n\n","\n")
            self.visuals.append(visual)
            scorer.score(pred_value, gold)
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
    
    def save(self):
        if self.out_dir is not None:
            self.out_dir = Path(self.out_dir)
        if not self.out_dir.exists():
            self.out_dir.mkdir()
        self.nlp.to_disk(self.out_dir)
        print("Modele saved in :", self.out_dir)

                
