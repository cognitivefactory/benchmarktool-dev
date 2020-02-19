import re
'''
rgx_str = "((\"\w+[^\"]*\")|(\'\w+[^']*'))"
key = "\[\([0-9]+,[0-9]+,"+rgx_str+"\)\]"
#rgx = '\('+rgx_str+',{\'entities\':'+key+'}\)'
rgx = '^\('+rgx_str+'$\)'
test = "('ok')"
text = "('Quel beau cheval!',{'entities':[(10,15,'animal')]})"
m = re.findall(rgx , test)
'''
f = open("../data/test_annotated", "r")
t = "[('Quel beau cheval', {'entities': [(10, 15, 'animal')]}), ('Le cheval.', {'entities': [(3, 8, 'animal')]})]"
f1 = f.read()
rgx_str = "((\"\w+[^\"]*\")|('\w+[^']*'))" 
rgx_key = "\[\(\s*[0-9]+\s*,\s*[0-9]+\s*,\s*"+rgx_str+"\s*\)\]"
pattern = '\('+rgx_str+',\s*{\'entities\':\s*'+rgx_key+'}\)'
rgx = '\['+pattern+'(,\s*'+pattern+')*(,\s*'+pattern+')?\]'
p = re.compile(rgx)
if p.match(f1):
    print(True)
else:
    print(False)
f.close()

print(p.split(f1))