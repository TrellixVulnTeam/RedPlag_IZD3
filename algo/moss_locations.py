""" \package MOSS With Locations
Plagiarism detector for source code files.
Detects plagiarism using Karp Rabin Hashing and winnowing
Marks overlapping hashes to exactly show the parts which where copied
"""

import numpy as np
q=1000000007

def intersection(lst1, lst2):
	"""!
        
	
	\details Finds hashes that are common to both lists and stores their location in both documents
	Finds similarity that is measured by 

	sim(A,B) = number of hashes in intersection of both hash sets divided by minimum of the number of hashes in lst1 and lst2
		
	\param  lst1 : 1st list whose elements are of the form (hash, document ID, character position)
	\param lst2: 2nd list whose elements are of the form (hash, document ID, character position)
	\return l3: list of common hashes and their locations in both documents. This is a list whose elements are of the form (common hash, (document ID1, location1), (documnet ID2, location2))
	\return sim: similarity measure evaluated
	"""
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l1loc = {h[0]:h[1:] for h in lst1}
	l2loc = {h[0]:h[1:] for h in lst2}
	
	l3h = list(set(l1h)&set(l2h))
	l3 = [(h, l1loc[h], l2loc[h]) for h in l3h] 
	sim = len(l3)/min(len(set(l1h)), len(set(l2h)))
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

def GetHLoc(t,id,k):
	"""!
       
        
	\details Reads the file in a single string and evaluate its k-grams. 
	For each k-gram, Karp-Rabin hash value is evaluated and stored in a list H. Along with the hashes, the location given by document ID and the character 
	at which the k-gram begins are stored
	
	\param t: file name
	\param id: document ID
	\param k: k-gram parameter
	
	\return H: The list H of hashes with their locations
	"""
	H = []
	infile = open(t,'r').read()
	infile = infile.rstrip('\n')
	
	for i in range(len(infile)-k):
		kgram = infile[i:i+k]
		h = 0
		for j in kgram: h = (256*h + ord(j))%q
		H.append((h,id,i))
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

def moss(files, t, k):
	n = len(files)
	H = [GetHLoc(files[i],i,k) for i in range(n)]
	HS = [Win(h,t,k) for h in H]
	strings = [open(files[i],'r').read().rstrip('\n')]

	C = np.identity(n)
	markings = []
	for i in range(n):
		max_overlap = -1.0
		max_overlap_index = -1
		for j in range(i):
			if C[i][j] > max_overlap: 
				max_overlap = C[i][j]
				max_overlap_index = j			
		for j in range(i+1, n):
			sim = similarity(HS[i], HS[j])
			C[i][j] = sim
			C[j][i] = sim
			if C[i][j] > max_overlap: 
				max_overlap = C[i][j]
				max_overlap_index = j
		intersect, s = intersection(HS[i], HS[max_overlap_index])
		markings_i = []
		for h in intersect:
				markings_i += [h[1][1]]
		markings += [markings_i]

	return C, markings
		
		
def moss_all_pairs(files, t, k):
	"""!
        \details Evaluates MOSS similarity and matching portions between each pair of files
        \param files: list of files
        \param t: Winnowing threshold parameter
        \param k: k-gram parameter
        \return C: similarity matrix such that C[i][j] denotes the similarity between the ith and jth file
        \return markings: markings matrix such that markings[i][j] is a list of charavter indices where matching k-grams begin for ith and jth file"""
	
	n = len(files)
	H = [GetHLoc(files[i],i,k) for i in range(n)]
	HS = [Win(h,t,k) for h in H]
	strings = [open(files[i],'r').read().rstrip('\n')]

	C = np.identity(n)
	markings = []
	for i in range(n):
		marks = []
		for j in range(n):
			marks += [[]]
		markings += [marks]
	
	for i in range(n):			
		for j in range(i+1, n):
			intersect,sim = intersection(HS[i], HS[j])
			C[i][j] = sim
			C[j][i] = sim
			for h in intersect:
				markings[i][j] += [h[1][1]]
				markings[j][i] += [h[2][1]]				

	return C, markings			
