# Importation des packages

from __future__ import unicode_literals, print_function
import plac #  wrapper over argparse
import random
from pathlib import Path
import spacy
from tqdm import tqdm # loading bar
from spacy import displacy

from spacy.gold import GoldParse
from spacy.scorer import Scorer

# Liste des entités que l'on voudra reconnaitre
LABEL = 'ANIMAL'

# Jeu d'entrainement 

TRAIN_DATA = [
    ("Quel beau cheval!", {
        'entities': [(10, 16, 'ANIMAL')]
    }),

    ("Le cheval.", {
        'entities': [(3, 9, 'ANIMAL')]
    }),

    ("Cheval blanc, cheval noir.", {
        'entities': [(0, 6, 'ANIMAL'),(14, 20, 'ANIMAL')]
    }),

    ("J'aime les chevaux.", {
        'entities': [(11, 17, 'ANIMAL')]
    }),

    ("Le cheval ne vaut pas l'avoine.", {
        'entities': [(3, 9, 'ANIMAL')]
    }),
    ("Monte sur ton cheval le plus noble.", {
        'entities': [(14, 20, 'ANIMAL')]
    }),
    ("Bride de cheval ne va pas à un âne..", {
        'entities': [(9, 15, 'ANIMAL'),(31, 34, 'ANIMAL')]
    }),
    ("On connaît le cheval en chemin, et le cavalier à l'auberge.", {
        'entities': [(14, 20, 'ANIMAL')]
    })
    
]

# Choix des paramètres

model = None# Si model = None alors nouveau modèle 
model_name = "Animal"# Nom du modèle
out_dir = None # répertoire où sauvegarder le modèle
nb_iter = 15 # nombre d'itérations

params = (model, model_name,TRAIN_DATA, LABEL, out_dir, nb_iter)

class Spacy_Model:
    def __init__(self,model,model_name, training_data,labels,out_dir, nb_iter):
        self.model_name = model_name
        self.nb_iter = nb_iter
        self.training_data = training_data
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
            
        self.ner.add_label(labels)
        if model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()
            
    def convert(self,data)
        spacyFormat = []
        lenData = len(data)
        lenEntities = 0

        #parsing the file & checking if it's correct
        for i in range(lenData):
            lenEntities = len(data[i]["entities"])
            for j in range(lenEntities):
                newDict ={}
                newDict['entities'] = [(data[i]["entities"][j][0], data[i]["entities"][j][1], data[i]["entities"][j][2])]
                spacyFormat.append((data[i]["text"], newDict))
        return spacyFormat
            
    def train(self):
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        with self.nlp.disable_pipes(*other_pipes):  # only train NER
            for itn in range(self.nb_iter):
                random.shuffle(self.training_data)
                losses = {}
                for text, annotations in tqdm(self.training_data):
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

# Création du modèle
model = Model(model, model_name,TRAIN_DATA, LABEL, out_dir, nb_iter)

#Entrainement du modèle
model.train()

# Test du modèle:
test_text = ("On dit qu\'un cheval est calme lorsqu'il limite l\'emploi de ses forces aux exigences de son cavalier. "
            "Tout travail entreprit sur un cheval irrité, impatient, inquiet, préoccupé de ce qui l\'entoure ou en crainte "
            "de son cavalier, ne peut être que mauvais. Le calme n\'est donc pas comparable à de"
            "l\'apathie et n'est pas le propre des chevaux manquant d\'influx nerveux. Un cheval endormi n\'est pas "
            "nécessairement un cheval calme et la résignation du cheval recherchée quelques fois par la mise en œuvre "
            "de procédures brutales n\'est pas non plus une source de calme. On a trop tendance à associer le calme à un "
            "\'manque de vie\', voire un obstacle à la performance sportive. C\'est tout le contraire, un cheval calme est "
            "vivant, réactif et ordonné.")

doc= model.test(test_text)

examples = [("On dit qu\'un cheval est calme",{
            'entities': [(13, 19, 'ANIMAL')]
            }),
            ("Un cheval endormi n\'est pas nécessairement un zèbre calme",{
             'entities': [(3, 9, 'ANIMAL'),(46,51, 'ANIMAL')]   
            })
           ]
res = model.evaluate(examples)

#ents_p = entities_precision
#ents_r = entities_recall
#ents_f = entities_f_score
print("precision : {}, recall : {}, f_score : {}".format(res['ents_p'],res['ents_r'], res['ents_f']))
