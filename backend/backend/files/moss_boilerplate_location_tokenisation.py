""" \package MOSS With Locations
Plagiarism detector for source code files.
Detects plagiarism using Karp Rabin Hashing and winnowing
Marks overlapping hashes to exactly show the parts which where copied
"""

import numpy as np
from pygments.lexers import guess_lexer_for_filename
import pygments
import sys
import os

q=1000000007

boiler_fingerprint = []

def tokenize(filename):
	"""!
	\details Tokenises a file according to it's extension. Replaces all variable identifiers by V, function names by F and strings by S
		Other words are taken as it is
		Stores starting index of each token in original and final file

	\param filename: Name of file with correct extension
	\return mapping: a list of tokens of the form [token , start index in original file, start index in tokenised file]
	"""
	with open(filename, 'r') as f:
		contents = f.read()
		tokens = list(guess_lexer_for_filename(filename, contents).get_tokens(contents))
		mapping = []
		n = len(tokens)
		
		a = 0
		b = 0
		
		for i in range(n):
			if tokens[i][0] == pygments.token.Name.Variable:
				mapping.append(['V', a, b])
				b = b + 1

			elif tokens[i][0] == pygments.token.Name.Function:
				mapping.append(['F', a, b])
				b = b + 1
			
			elif tokens[i][0] == pygments.token.Literal.String:
				mapping.append(['S',a,b])
				b = b + 1

			elif tokens[i][0] != pygments.token.Text and tokens[i][0] != pygments.token.Comment:
				mapping.append([tokens[i][1], a, b])
				b = b + len(tokens[i][1])
			a = a + len(tokens[i][1])
		return mapping

def intersection(lst1, lst2):
	"""!
        
	
	\details Finds hashes that are common to both lists and stores their location in both documents
	Finds similarity that is measured by 

	sim(A,B) = number of hashes in intersection of both hash sets divided by minimum of the number of hashes in lst1 and lst2
		
	\param  lst1 : 1st list whose elements are of the form [hash, start location, end location]
	\param lst2: 2nd list whose elements are of the form [hash, start location, end location]
	\return l3: list of common hashes and their locations in both documents. This is a list whose elements are of the form 
		[common hash, [start location in 1, end location in 1], [start location in 2, end location in 2]]
	\return sim: similarity measure evaluated
	"""
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l1loc = {h[0]:h[1:] for h in lst1}
	l2loc = {h[0]:h[1:] for h in lst2}
	
	l3h = list(set(l1h)&set(l2h))
	l3 = [[h, l1loc[h], l2loc[h]] for h in l3h] 
	sim = len(l3)/min(len(set(l1h)), len(set(l2h)))
	return l3, sim

def intersection_minus_boilerplate(lst1, lst2):
	"""!
	\details Finds hashes that are common to both lists and stores their locations in both documents.
	Also considers the fingerprint of boilerplate code and those hashes are not considered as part of the documents while evaluating similarity
	
	Finds similarity that is measured by 

	sim(A,B) = number of hashes in intersection of both hash sets divided by minimum of the number of hashes in lst1 and lst2
	\param  lst1 : 1st list whose elements are of the form [hash, start location, end location]
	\param lst2: 2nd list whose elements are of the form [hash, start location, end location]
	\return l3: list of common hashes and their locations in both documents. This is a list whose elements are of the form 
		[common hash, [start location in 1, end location in 1], [start location in 2, end location in 2]]
	\return sim: similarity measure evaluated
	"""

	l1h = [h[0] for h in lst1]
	l2h = [h[0] for h in lst2]
	l1loc = {h[0]:h[1:] for h in lst1}
	l2loc = {h[0]:h[1:] for h in lst2}

	boiler = set([h[0] for h in boiler_fingerprint])
	
	l3h = list(set(l1h)&set(l2h))
	l3h_without_boiler = [h for h in l3h if h not in boiler]

	l1h_without_boiler = set([h for h in l1h if h not in boiler])
	l2h_without_boiler = set([h for h in l2h if h not in boiler])

	sim = len(l3h)/min(len(l1h_without_boiler), len(l2h_without_boiler))
	l3 = [[h, l1loc[h], l2loc[h]] for h in l3h] 
	return l3, sim

def similarity(lst1, lst2):
	"""!
		\details Evaluates similarity as done in intersection function but doesn't return locations of common hashes
	"""
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l3h = list(set(l1h)&set(l2h))
	sim = len(l3h)/min(len(set(l1h)), len(set(l2h)))
	return sim

def GetHLoc(t,k):
	"""!
       
        
	\details Reads the file and tokenises it. Evaluate its k-grams. 
	For each k-gram, Karp-Rabin hash value is evaluated and stored in a list H. Along with the hashes, the location information given by start and end location of the k-gram in both initial and tokenized files are stored
	
	\param t: file name
	\param k: k-gram parameter
	
	\return H: The list H of hashes with their locations
	"""
	H = []
	mapping = tokenize(t)
	current_length = 0
	kgram = ""
	kgrams = []
	start_locs = []
	end_locs = []
	i = 0

	while i < len(mapping):
		if kgram == "":
			start_locs += [(mapping[i][1], mapping[i][2])]

		if current_length + len(mapping[i][0]) > k:
			deficit = k - current_length
			kgram = kgram + mapping[i][0][:deficit]
			kgrams += [kgram]
			end_locs += [[mapping[i][1], mapping[i][2]]]
			mapping[i][0] = mapping[i][0][deficit:]
			current_length = 0
			kgram = ""

		elif current_length + len(mapping[i][0]) == k:
			kgram = kgram + mapping[i][0]
			kgrams += [kgram]
			end_locs += [[mapping[i][1], mapping[i][2]]]
			current_length = 0
			kgram = ""
			i = i + 1

		else:
			kgram = kgram + mapping[i][0]
			current_length += len(mapping[i][0])
			i = i + 1
			if i == len(mapping):
				kgrams += [kgram]
				end_locs += [[mapping[i-1][1], mapping[i-1][2]]]

	for j in range(len(kgrams)):
		h = 0
		for k in kgrams[j]: h = (256*h + ord(k))%q
		H.append([h,start_locs[j], end_locs[j]])
	return H
    
    

def Win(H,t,k):
	"""!
        \details Applies Winnowing algorithm on given list of hashes with a window size such that for every substring of length t we will pick atleast one hash.
        Also stores the locations of selected hashes

        \param H: List of (hash, document ID, location)
        \param t: Winnowing threshold parameter
        \param k: k-gram parameter used while calculating hashes

        \return HS: Selected (winnowed) hashes
	"""
	HS=[]
	w=t+1-k
	n=len(H)
	mI=-1
	pmI=-1

        if(len(H) < w):
                if (len(H) > 0):
                    HS.append(H[0])
                else:
                    HS.append(q)

	
	for i in range(0,len(H)-w+1):
		tm=9223372036854775807
		for j in range(i, i+w):
			if H[j][0]<=tm:
				mI=j
				tm=H[j][0]
		if mI != pmI:
			pmI=mI
			HS.append(H[mI])
	return HS
		
		
def moss_all_pairs(files, boilerplate, t, k):
	"""!
        \details Evaluates MOSS similarity and matching portions between each pair of files
        \param files: list of files
        \param t: Winnowing threshold parameter
        \param k: k-gram parameter
        \return C: similarity matrix such that C[i][j] denotes the similarity between the ith and jth file
        \return markings: markings matrix such that markings[i][j] is a list of charavter indices where matching k-grams begin for ith and jth file"""
	
	n = len(files)
	boiler_fingerprint = Win(GetHLoc(boilerplate,k),t,k)
	H = [GetHLoc(f,k) for f in files]
	HS = [Win(h,t,k) for h in H]

	C = np.identity(n)
	markings = []
	for i in range(n):
		marks = []
		for j in range(n):
			marks += [[]]
		markings += [marks]
	
	for i in range(n):			
		for j in range(i+1, n):
			intersect,sim = intersection_minus_boilerplate(HS[i], HS[j])
			C[i][j] = sim
			C[j][i] = sim
			for h in intersect:
				markings[i][j] += [(h[1][0][0],h[1][1][0])]
				markings[j][i] += [(h[2][0][0],h[2][1][0])]				

	return C, markings

folder = sys.argv[1]
print(os.getcwd())
bo = sys.argv[2]
files = os.listdir(folder)
paths = [folder + '/' + f for f in files]
t = 10
k = 5
print(moss_all_pairs(paths,bo,t,k))
