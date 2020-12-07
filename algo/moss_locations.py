""" \package MOSS With Locations
Plagiarism detector for source code files.
Detects plagiarism using Karp Rabin Hashing and winnowing
Marks overlapping hashes to exactly show the parts which where copied
"""

import numpy as np
q=1000000007

def intersection(lst1, lst2):
	"""!
	\brief Finds instersection of set of hashes and their locations
	
	\details Finds hashes that are common to both lists and stores their location in both documents
	Finds similarity that is measured by \f[
	sim(A,B) = \frac{\left | A \cap B\right |}{min \left(\ \left | A \right | , \left | B \right | right)}\f]
		
	\param  lst1 ,lst2: 2 lists whose elements are of the form (hash, document ID, character position)
	\return l3: list of common hashes and their locations in both documents. This is a list whose elements are of the form (common hash, (document ID1, location1), (documnet ID2, location2)
	sim: similarity measure evaluated
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
		\details Evaluates similarity as done in $intersection function but doesn't return locations of common hashes"""
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l3h = list(set(l1h)&set(l2h))
	sim = len(l3h)/min(len(set(l1h)), len(set(l2h)))
	return sim

def GetHLoc(t,id,k):
	""" !
		\details Reads the file in a single string and evaluate its k-grams. 
	For each k-gram, Karp-Rabin hash value is evaluated and stored in a list H. Along with the hashes, the location given by document ID and the character 
	at which the k-gram begins are stored
	
		\param
		t: file name
		id: document ID
		k: k-gram parameter
		
		\return
		H: The list H of hashes with their locations"""
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
	"""Given a list $H that contains the result of GetHLoc function, i.e. a list whose elements are of the form (hash, document ID, character position),
		a threshold parameter $t and k-gram parameter $k, function applies Winnowing algorithm on a window size such that for every substring of length $t we pick a hash.
		
	Returns a list $HS that has selected (winnowed) some elements of $H by the above method"""
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
	""" Given a list of files, threshold parameter $t and k-gram parameter $k, 
	evaluates for every pair, the MOSS similarity and 
	stores matching hashes into matrices C and markings respectively"""
	
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
