""" \package MOSS With Locations
Plagiarism detector for source code files.
Detects plagiarism using Karp Rabin Hashing and winnowing
Marks overlapping hashes to exactly show the parts which where copied
"""

import numpy as np
q=1000000007

def intersection(lst1, lst2):
	"""Input: 2 lists $lst1 and $lst2 whose elements are of the form (hash, document ID)Finds hashes that are common to both $lst1 and $lst2"""
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l1loc = {h[0]:h[1:] for h in lst1}
	l2loc = {h[0]:h[1:] for h in lst2}
	
	l3h = list(set(l1h)&set(l2h))
	l3 = [(h, l1loc[h], l2loc[h]) for h in l3h] 
	sim = len(l3)/min(len(set(l1h)), len(set(l2h)))
	return l3, sim

def similarity(lst1, lst2):
	l1h = [h[0] for h in lst1] 
	l2h = [h[0] for h in lst2]
	l3h = list(set(l1h)&set(l2h))
	sim = len(l3h)/min(len(set(l1h)), len(set(l2h)))
	return sim

def GetHLoc(t,id,k):
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
