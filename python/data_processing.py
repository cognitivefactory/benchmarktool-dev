import re
from os import chdir, getcwd
wd=getcwd()
chdir(wd)

'''
    Creation of the annotated data
    > create a file entitled filename_annoted
    > create a data structure with annotations
    input : 
        filename -- string : name of the file
        target -- list of string : target words
        label -- list of string : labels of target words
    Output : 
        data : data structure with annotations
        
'''
def create_annoted_data(filename, target, label):
    f = open(filename, "r")
    l_target = len(target)
    l_label = len(label)
    if not f or l_target==0 or l_label==0 or l_target!=l_label:
        return None
    data = []
    new_file = open(filename+"_annotated", "w")
    if not new_file:
        return None
    strs = list(f.read().splitlines())
    for e in strs:
        for i,t in enumerate(target):
            if t in e.lower():
                start = (e.lower()).index(t)
                end = start + len(t) - 1
                data.append((e,{'entities':[(start, end, label[i])]}))
    
    new_file.write(str(data))
    return data

'''
    #Train/test split dataset
    > Split the dataset in two
    input : 
        data : data structure with annotations
        training_proportion -- float between 0 and 1 : 
            proportion of the data used for the training
    output : 
        train, test : two datasets
'''
def train_test_split(data, training_proportion):
    l_data = len(data)
    train_proportion = int(training_proportion * l_data)
    #0.6 => 60% of the data will be used for the training
    
    return data[:train_proportion], data[train_proportion:]



txt = "(\"aze\",'entities':[12,2,\"animal\"])"
regex = "\(\".+\",\'entities\':\[[0-9]+,[0-9]+,\".+\"\]\)"
x = re.findall(regex, txt) 


if (x):
  print("YES! We have a match!")
else:
  print("No match")