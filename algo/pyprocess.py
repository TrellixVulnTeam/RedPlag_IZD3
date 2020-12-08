import sys, token, tokenize
import re
import os


def do_file(filename):
    """ Run on just one file.
    """
    infile = open(filename, 'r').read()
    infile = re.sub('\"\"\".*\"\"\"', '', infile, flags=re.S)
    infile = re.sub('\'\'\".*\"\"\"', '', infile, flags=re.S)
    infile = re.sub('\#.*?\n', '', infile, flags=re.S)
    infile = re.sub('([\t]+\n)','',infile)
    results = re.sub('([\n]+)','\n',infile)
    results2 = re.sub(r'\^import.*', '', results)
    open(filename, 'w').write(results2)


def replace_function(filename):
    """
    Replace non recursive function calls in the code with the function definition
    Detects all the funtions in the code
    Identifies function calls and replaces with the function definition
    """
    #identifying functions
    infile = open(filename, 'r')
    L = []
    i = 1
    previous = ""
    for line in infile:
        if previous!="" and previous.startswith('def'):
            f_name = previous[4:].split('(')[0].strip()
            num = len(previous[4:].split('(')[1].split(')')[0].split(','))
            start = i-1
            end = 0
            lines = []
            rec = 0
            lines.append(line)
            p = 0
            for line in infile:
                if line.startswith('\t'):
                    if(line.find(f_name)):
                        rec = 1
                    lines.append(line)
                    i = i+1
                else:
                    p = 1
                    end = start+len(lines)
                    L.append([f_name, num, start, end, lines, rec])
                    previous = line
                    i = i+1
                    break
            if p == 0:
                end = start + len(lines)
                L.append([f_name, num, start, end, lines, rec])
        elif line.startswith('def'):
            f_name = line[4:].split('(')[0].strip()
            num = len(line[4:].split('(')[1].split(')')[0].split(','))
            start = i
            end = 0
            rec = 0
            lines = []
            p = 0
            for line in infile:
                if line.startswith('\t'):
                    if(line.find(f_name)!=-1):
                        rec = 1
                    lines.append(line)
                    i = i+1
                else:
                    p = 1
                    previous = line
                    end = start + len(lines)
                    L.append([f_name, num, start, end, lines, rec])
                    i = i+1
                    break
            if p == 0:
                end = start + len(lines)
                L.append([f_name, num, start, end, lines, rec])
        i = i + 1
    # print(L)
    infile.close()
    # replacing functions:
    for i in range(0, 4):
        infile2 = open(filename, 'r').readlines()
        for line in infile2:
            if line.startswith('\t'):
                for item in L:
                    if item[-1]!=1:
                        f = line.find(item[0])
                        if f!=-1:
                            idx = infile2.index(line)
                            infile2[idx] = ''.join(item[4])
        open(filename, 'w').write(''.join(infile2))
    fun_list = []
    for item in L:
        fun_list.append(item[0]) 
    return fun_list       

def replace_variables(filename, func_names = []):
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

    infile = open(filename, 'r').read()
    infile_temp = infile
    x = []
    y = []
    i=0
    while i<len(infile):
        m = re.search(r"(\W|\b)([a-zA-Z]+[\w]*)(\W|\b)", infile[i:])
        if m!=None:
            x.append(m.group(2))
            y.append(m.start() + i)
            i = i + m.end() -1
        else:
            break

    var = []
    var_loc = []

    for i in range(0, len(x)):
        if x[i] not in keywords and x[i] not in func_names:
            var.append(x[i])
            var_loc.append(y[i])

    var.reverse()
    var_loc.reverse()
    for i in range(0, len(var)):
        start = var_loc[i] + 1
        end = start + len(var[i])
        infile = infile[:start] + 'v' + infile[end:]

    outfile = open(filename, 'w')
    outfile.write(infile)
    outfile.close()

def boiler(bo, co):
    ##Remove the boiler plate code from the given file
    #
    # @param bo: boiler plate file
    # @param co: code file
    infile = open(bo)
    ct=0;
    for line in infile :
        skip=False
        if line.find("def")!=-1:
            skip=True
        
        if skip==False:
            with open(co, "r+") as f:
                d = f.readlines()
                f.seek(0)
                done=False
                for i in d:
                    if i != line or done==True:
                        f.write(i)
                    else:
                        done=True
                f.truncate()

def stripspaces(filename):
    """
    Removes multiple spaces and adds spaces around variables
    """
    infile = open(filename, 'r').read()
    infile = re.sub('([^a-zA-Z0-9\s]+)', ' \\1 ', infile)
    infile = re.sub('([\s]+)', ' ', infile)
    open(filename, 'w').write(infile)


def preprocess(filename, b=False, bo="none.txt"):
    """
    Removes comments, replaces functions, strip spaces and replace variables
    """
    try:
        if b==True:
            boiler(bo,filename)
    except:
        print('boilerplate')
    try:
        do_file(filename)
    except:
        print('comments')
    try:
        func_names = replace_function(filename)
    except:
        print('replace function')
    try:
        stripspaces(filename)
    except:
        print('strip spaces')
    try:
        replace_variables(filename, func_names)
    except:
        print('replace variables')