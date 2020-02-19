import re
from os import chdir, getcwd
wd=getcwd()
chdir(wd)

'''
    CREATE_ANNOTATION
        for a given file, create a new one entitled filename_annotated
        which contains annotations
    Return : data structure with annotations      
'''
def create_annotation(filename, lst_target, lst_label):
    f = open(filename, "r")
    l_target = len(lst_target)
    l_label = len(lst_label)
    if not f or l_target==0 or l_label==0 or l_target!=l_label:
        return False
    
    new_file = open(filename+"_annotated", "w")
    if not new_file:
        return False
    data = []
    strs = list(f.read().splitlines())
    
    for e in strs:
        for i,t in enumerate(lst_target):
            if t in e.lower():
                start = (e.lower()).index(t)
                end = start + len(t) - 1
                data.append((e,{'entities':[(start,end,lst_label[i])]}))
    new_file.write(str(data))
    new_file.close(); f.close()
    return True




'''
    CHECK_ANNOTATION
        for a given file, check if content matches our annotations standard
        using REGEX to find the pattern :
            ("or' string 'or", 'entities':[(nb,nb,"or' string "or')]})
    Return : bool
    
    
'''
def check_annotation(filename):
    f = open(filename, "r")
    f1 = f.read()
    f.close()
    rgx_str = "((\"\w+[^\"]*\")|('\w+[^']*'))" 
    rgx_key = "\[\(\s*[0-9]+\s*,\s*[0-9]+\s*,\s*"+rgx_str+"\s*\)\]"
    pattern = '\('+rgx_str+',\s*{\'entities\':\s*'+rgx_key+'}\)'
    rgx = '\['+pattern+'(,\s*'+pattern+')*(,\s*'+pattern+')?\]'
    p = re.compile(rgx)
    if p.match(f1):
        return True
    else:
        return False

'''
filename = "../data/my_data"
if not create_annotation(filename, ["cheval"], ["animal"]):
    print("Error : File cannot be created")
else:
    if not check_annotation(filename+"_annotated"):
        print("Error : the file doesn't match the standard")
'''



