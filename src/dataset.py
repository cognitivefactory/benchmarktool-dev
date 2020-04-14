class Dataset:
    def __init__(self, title="dataset"):
        self.title = title
        self.nEntities = 0
        self.mostCommon = []
        return
    
    def __del__(self): 
        print("destruction of the dataset")
        
    def __repr__(self):
        return {'title "':self.title, '" nEntitities':self.nEntities, 'lstEntities':self.mostCommon}
      
    def __str__(self):
        return 'the dataset "'+self.title+'" has '+str(self.nEntities)+' entities.'
        
        
    
    def printTitle(self):
        return self.title
    
    def printNEntities(self):
        return self.nEntities
    
    def printMostCommon(self):
        return self.mostCommon
        
    def isCorrect(self, data):
        self.nEntities = 0
        labels = []
        lenData = len(data)
        lenEntities = 0
        
        #parsing the file & checking if it's correct
        for i in range(lenData):
            if not data[i]["text"]:
                print("error, the text is empty\n")
                return False
            lenEntities = len(data[i]["entities"])
            #for each entity
            for j in range(lenEntities):
                if data[i]["entities"][j][0] > data[i]["entities"][j][1]:
                    print("error, incorrect index\n")
                    return False
                if not data[i]["entities"][j][2]:
                    print("error, the label is empty\n")
                    return False
                labels.append(data[i]["entities"][j][2])
            self.nEntities += lenEntities              

        #Find most common labels
        dic = {}
        for word in labels:
            dic.setdefault(word, 0)
            dic[word] += 1
        labelList = [(dic.get(w), w) for w in dic]
        if self.nEntities < 5 : 
            self.mostCommon = labelList
        else:
            self.mostCommon = labelList[:5]
        return True