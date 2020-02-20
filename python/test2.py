import re

t = "[('Quel beau cheval', {'entities': [(10, 15, 'animal')]},{),('Quel beau cheval', {'entities': [(10, 15, 'animal')]})]"
rgx_str = "((\"\w+[^\"]*\")|('\w+[^']*'))"
rgx_dict = "(\s*,\s*{[^}]*})*"          
rgx_key = "\[\(\s*[0-9]+\s*,\s*[0-9]+\s*,\s*"+rgx_str+"\s*\)\]}"
pattern = '\('+rgx_str+',\s*{\'entities\':\s*'+rgx_key+rgx_dict+'\)'
rgx = '\['+pattern+'(,\s*'+pattern+')*(,\s*'+pattern+')?\]'
p = re.compile(rgx)
if p.match(t):
    print(True)
else:
    print(False)