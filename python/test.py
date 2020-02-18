import re

rgx_str = "((\"\w+[^\"]*\")|(\'\w+[^']*'))"
key = "\[\([0-9]+,[0-9]+,"+rgx_str+"\)\]"
rgx = '\('+rgx_str+',{\'entities\':'+key+'}\)'
text = "('Quel beau cheval!',{'entities':[(10,15,'animal')]}), ('Cheval!',{'entities':[(0,5,'animal')]})"
m = re.findall(rgx , text)
print()