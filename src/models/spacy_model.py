from model import *

#spaCy imports
import spacy
from tqdm import tqdm
from spacy import displacy
from spacy.scorer import Scorer
import random
from spacy.gold import GoldParse


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
            

        if self.model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()

        labels = [ label for label in self.training_data.labels]
        for l in labels :
            self.ner.add_label(l)

        self.training_data = self.convert_format(self.training_data)
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        
        with self.nlp.disable_pipes(*other_pipes):
            training_loss = []
            for _ in range(self.nb_iter):
                random.shuffle(self.training_data)
                losses = {}
                
                for text, annotations in tqdm(self.training_data):
                    self.nlp.update([text], [annotations], sgd=self.optimizer, drop=0.35,
                        losses=losses)
                print(losses)
                training_loss.append(losses["ner"])
            print(training_loss)
        self.losses = training_loss
        self.is_ready = 1

                
    def test(self, test_data):
        data = self.convert_format(test_data)
        res={"model_name" : self.model_name}
        scorer = Scorer()
        for sents, ents in data:
            doc_gold = self.nlp.make_doc(sents)
            gold = GoldParse(doc_gold, entities=ents['entities'])
            pred_value = self.nlp(sents)
            visual = displacy.render(pred_value, style="ent")
            visual = visual.replace("\n\n","\n")
            self.visuals.append(visual)
            scorer.score(pred_value, gold)
            score = scorer.scores
        res["precision"] = score["ents_p"]
        res["recall"] = score["ents_r"]
        res["f_score"] = score["ents_f"]
        score["ents_per_type"]
        res["score_by_label"] = score["ents_per_type"]
        return res

    """save : not used for now
    def save(self):
        if self.out_dir is not None:
            self.out_dir = Path(self.out_dir)
        if not self.out_dir.exists():
            self.out_dir.mkdir()
        self.nlp.to_disk(self.out_dir)
        print("Modele saved in :", self.out_dir)
    """