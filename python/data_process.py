import re
from os import chdir, getcwd
wd=getcwd()
chdir(wd)

'''
    FILE_ANNOTATION
    > create a file entitled filename_annotated
    > create a data structure with annotations
    input : 
        filename -- string
        target -- list of string : target words
        label -- list of string : labels of target words
    Output : 
        data : data structure with annotations      
'''
def file_annotation(filename, target, label):
    f = open(filename, "r")
    l_target = len(target)
    l_label = len(label)
    if not f or l_target==0 or l_label==0 or l_target!=l_label:
        return False
    
    new_file = open(filename+"_annotated", "w")
    if not new_file:
        return False
    data = []
    strs = list(f.read().splitlines())
    
    for e in strs:
        for i,t in enumerate(target):
            if t in e.lower():
                start = (e.lower()).index(t)
                end = start + len(t) - 1
                data.append((e,{'entities':[(start,end,label[i])]}))
    new_file.write(str(data))
    new_file.close(); f.close()
    return True




'''
    CHECK_ANNOTATION
        
'''
def check_annotation(text):








