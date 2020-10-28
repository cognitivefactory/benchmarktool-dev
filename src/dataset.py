""" Dataset : Parent class - check and store the data structure of an annotated JSON file.
    TrainData : Child class - specific to training dataset: allow to store metadata.
"""

import json
import re
import hashlib
import random
import os

#### Dataset

class Dataset(object):

    def __init__(self, title=""):
        self.title = title
        
    def filter_json(self, json_file):
        """keep only the text elements and entities of the JSON file."""
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
        
               
        self.file = file        
        return True
    
    
    def is_correct(self):
        """check if the content of the file is correct."""

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
    def __init__(self, title=""):
        Dataset.__init__(self, title=title)
        self.hash = ""
        self.nb_entities = 0
        self.labels = []
        
    def __str__(self):
        """print(obj)"""
        return 'the dataset "'+ self.title +'" has '+ str(self.nb_entities) +' entities.'
    
    
    def metadata(self):
        """complete the object properties to create metadata."""       
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


    def from_metadata(self, meta_content):
        """fill object properties from a metadata file."""
        self.title = meta_content['title']
        self.hash = meta_content['hash']
        self.file = meta_content['file']
        self.nb_entities = meta_content['nb_entities']
        self.labels = meta_content['labels']
    
    def metafile_exists(self):
        """Check if a file already exists for this training dataset."""
        path = "./datasets/"
        metafiles = os.listdir(path)
        for metafile in metafiles:
            with open(path + "/" + metafile, encoding='utf-8') as json_file:
                data = json.load(json_file)
                if data['hash'] == self.hash:
                    return True

        return False

    
    def create_metafile(self):
        """create a file with the metadata."""
        
        if(not self.metafile_exists()):
            path = "./datasets/"

            meta = {}
            meta['title'] = self.title
            meta['hash'] = self.hash
            meta['file'] = self.file
            meta['nb_entities'] = self.nb_entities
            meta['labels'] = self.labels
            with open(path + self.title + '.json', 'w') as outfile:
                json.dump(meta, outfile)
            print("metafile created")

        else:
            print("metafile already exists")
