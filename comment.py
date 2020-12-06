import re

def stripcomments(text):
    txt = re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)
    txt = re.sub('([^a-zA-Z0-9\s]+)', ' \\1 ', txt)
    txt = re.sub('([\s]+)', ' ', txt)
    return txt


infile = open("ts.txt", 'r').read()
print(stripcomments(infile))
