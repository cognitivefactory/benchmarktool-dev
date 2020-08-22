""" Dataset : Parent class - checks and stores the data structure of an annotated JSON file.
    TrainData : Child class - specific to training dataset: allows to store metadata.
"""

import json
import re
import hashlib
import random

#### Dataset

class Dataset(object):
    def __init__(self, title):
        self.title = title
        
    def filter_json(self, json_file):
        """keeps only the text elements and entities of the JSON file"""
        file = []
        for o in json_file:
            try:
                text = o['text']
                try:
                    entities = o['entities']
                    if not text or not entities : 
                        return

                except:
                    return
            except:
                return
            obj = {'text' : text, 'entities' : entities}
            file.append(obj)
        
        random.shuffle(file)        
        self.file = file        
        return True
    
    
    def is_correct(self):
        """checks if the content of the file is correct"""

        r_str = "((\"[^\"]+\")|(\'[^\']+\'))"
        r_entity = "\[\d+,\s*\d+,\s*" + r_str + "\]"
        for obj in self.file:
            entity = obj['entities']
            if not entity :
                return False
            for e in entity:
                if not re.fullmatch(r_entity, str(e)) or e[0] >= e[1]:
                    return False
        return True


#### TrainData

class TrainData(Dataset):
    def __init__(self, title):
        Dataset.__init__(self, title)
        self.hash = ""
        self.nb_entities = 0
        self.labels = []
        
    def __str__(self):
        """print(obj)"""
        return 'the dataset "'+ self.title +'" has '+ str(self.nb_entities) +' entities.'
    
    
    def metadata(self):
        """completes the object properties to create metadata"""       
        dic = {}
        nb_entities = 0
        for obj in self.file:
            self.nb_entities += len(obj['entities'])
            for e in obj['entities']:
                dic.setdefault(e[2], 0)
                dic[e[2]] += 1
        self.labels = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse = True)}        
            
        #MD5 hash - encoded data in hexadecimal format.
        self.hash = hashlib.md5(str(self.file).encode()).hexdigest()
        return True
    
    def create_metafile(self):
        meta = {}
        meta['title'] = self.title
        meta['hash'] = self.hash
        meta['file'] = self.file
        meta['nb_entities'] = self.nb_entities
        meta['labels'] = self.labels
        #TODO : vérifier si le fichier existe déjà ou non
        with open("datasets/"+self.title+'.json', 'w') as outfile:
            json.dump(meta, outfile)
            return True
        return False