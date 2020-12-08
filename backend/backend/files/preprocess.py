import re
import sys

## @brief Preprocesses the cpp input file before plag check
#
# Removes Comments, #define declarations, headers
# Makes the code white space insensitive.
# Replace every variable/class/any other user defined name by N, Replace every string literal by S, Replace every function name by F

## Removes Commented portions of the code, namespaces and includes
#
# @param filename: location of file whose comments need to be removed
# \return void: Modifies the input file
def stripcomments(filename):
	try:
		infile = open(filename, 'r').read()
		infile = re.sub('//.*?\n|/\*.*?\*/|\#include.*?\n|using.*?\n', '', infile, flags=re.S)
		open(filename, 'w').write(infile)
	except:
		print('could not strip comments')
		return

## Removes the #define directives from the code and replaces them in the code with the specifies word
#
# @param filename: location of cpp file whose #define directives need to be replaced
# @return void: modifies the input file
def replace_define(filename):
	try:
		infile = open(filename, 'r')
		out = ""
		define = []
		definition = []
		for l in infile:
			for i in range(0, len(define)):
				x = []
				y = []
				j = 0
				while j<len(l):
					match = re.search(r"(\W|\b)(" + define[i] + ")(\W|\b)", l[j:])
					if match!=None:
						x.append(match.group(2))
						y.append(match.start() + j)
						j = j + match.end() - 1
					else:
						break
				x.reverse()
				y.reverse()
				for k in range(0, len(y)):
					start = y[k] + 1
					end = start + len(define[i])
					l = l[:start] + definition[i] + l[end:]
			t = 0
			if l.startswith("#define"):
				items = l.split(' ')
				define.append(items[1].strip())
				definition.append(items[2].strip())
				t = 1
			if t ==0:
				out = out + l

		infile.close()
		outfile = open(filename, 'w')
		outfile.write(out)
		outfile.close()
	except:
		print("#define")
		return

## Remove the boiler plate code from the given file
#
# @param bo: location of boilerplate file
# @param co: given code file from which boiler plate needs to be removed

def boiler(bo, co):
	infile = open(bo, encoding = 'utf-8')
	ct=0;
	s1=["void","int","bool","char","float","double","long"]
	for line in infile :
		skip=False
		if line.find('(')!=-1 and line.find(';')==-1:
			if line.find('{')!=-1:
				ct=ct+1
			if line.find('for')==-1 and line.find('while')==-1:
				skip=True
		elif line.find('{')!=-1:
			ct=ct+1
			if(ct==1):
				skip=True
		elif line.find('}')!=-1:
			ct=ct-1
			if ct==0:
				skip=True
		if skip==False:

			with open(co, "r+",  encoding = 'utf-8') as f:

			    d = f.readlines()
			    f.seek(0)
			    done=False
			    for i in d:
			        if i != line or done==True:
			        	f.write(i)
			        else:
			        	done=True
			    f.truncate()

import pygments
import pygments.lexers

def tokenize(filename):
    """! @brief Tokenize input file
    
    Remove comments, Replace every variable/class/any other user defined name by N, Replace every string literal by S, Replace every function name by F
    
    \param filename: path of the file to be tokenized
    
    \return result: Every token is a string, obtained by stripping the file content to words and performing the cleaning described. The starting index of the token in the cleaned code and actual code are also stored
    """
    file = open(filename, "r")
    text = file.read()
    file.close()
    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    tokens = lexer.get_tokens(text)
    tokens = list(tokens)
    result = []
    lenT = len(tokens)
    count1 = 0    #tag to store corresponding position of each element in original code file
    count2 = 0    #tag to store position of each element in cleaned up code text
    # these tags are used to mark the plagiarized content in the original code files.
    for i in range(lenT):
        if tokens[i][0] == pygments.token.Name and not i == lenT - 1 and not tokens[i + 1][1] == '(':
            result.append(('N', count1, count2))  #all variable names as 'N'
            count2 += 1
        elif tokens[i][0] in pygments.token.Literal.String:
            result.append(('S', count1, count2))  #all strings as 'S'
            count2 += 1
        elif tokens[i][0] in pygments.token.Name.Function:
            result.append(('F', count1, count2))   #user defined function names as 'F'
            count2 += 1
        elif tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment:
            pass   #whitespaces and comments ignored
        else:
            result.append((tokens[i][1], count1, count2))  
            #tuples in result-(each element e.g 'def', its position in original code file, position in cleaned up code/text) 
            count2 += len(tokens[i][1])
        count1 += len(tokens[i][1])

    return result

def preprocess(filename, b=False, bo="none.txt"):
	"""
	Removes boiler plate if provided, then strips comments, replaces function calls, removes #defines, removes multiple spaces
	Replace variable by 'v'
	"""
	try:
		if b==True:
			boiler(bo,filename)
		file = open(filename, "r")
		text = file.read()
		file.close()
		from pygments.lexers.c_cpp import CppLexer
		lexer = CppLexer()
		tokens = lexer.get_tokens(text)
		tokens = list(tokens)
		result = ""
		lenT = len(tokens)

		for i in range(lenT):
		    if tokens[i][0] == pygments.token.Name and not i == lenT - 1 and not tokens[i + 1][1] == '(':
		        result += 'V'
		    elif tokens[i][0] in pygments.token.Literal.String:
		        result += 'S'
		    elif tokens[i][0] in pygments.token.Name.Function:
		        result += 'F'
		    elif tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment:
		        pass   #whitespaces and comments ignored
		    else:
		        result += tokens[i][1]
		open(filename, 'w').write(result)
	except:
		return