
class Spacy_Model:
    """Class to train/test a model using spaCy"""
    
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
            
        for l in labels :
            self.ner.add_label(l)
        if model is None:
            self.optimizer = self.nlp.begin_training()
        else:
            self.optimizer = self.nlp.entity.create_optimizer()


class Flair_Model:
     """Class to train/test a model using flair"""
    
    def __init__(self,model_name, training_data, nb_iter=10, lr=0.1, batch=32, mode='cpu'):
        
        self.model_name = './'+ model_name
        self.nb_iter = nb_iter
        self.learning_rate=lr
        self.batch_size=batch
        self.mode=mode
        self.training_data = training_data
        


    def train(self):
        self.convert_format()
        corpus: Corpus = ColumnCorpus(data_folder, {0: 'text', 1: 'ner'},
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
                                                tag_type=tag_type,
                                                use_crf=True)
        self.trainer = ModelTrainer(tagger, corpus)
        trainer.train(self.model_name,learning_rate=self.learning_rate,mini_batch_size=self.batch_size, max_epochs=self.nb_iter,embeddings_storage_mode=self.mode)




    def test(self, test_data):
        model = SequenceTagger.load(self.model_name+'/best-model.pt')

        corpus: Corpus = ColumnCorpus(data_folder, {0: 'text', 1: 'ner'},
                                        train_file=None,
                                        test_file=test_data
                                      )
        result, eval_loss = model.evaluate(corpus.test)
        # permet de retourner un dictionnaire de la même forme que celui fourni pas spaCy
        res = result.detailed_results
        res = res.split('\n')[:][9:-4]
        res =' '.join(str(res).split())
        res = res.replace("[\'",'')
        res = res.replace("\']",'')
        res = res.replace("', '",'')
        res = res.split()
        scores = {}
        for i in range(0,len(res),5):
            scores[res[i]] = {}
            scores[res[i]]['p'] = res[i+1]
            scores[res[i]]['r'] = res[i+2]
            scores[res[i]]['f'] = res[i+3]
        return scores
        