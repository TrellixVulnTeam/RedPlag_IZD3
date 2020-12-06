import numpy as np
q=1000000007

def intersection(lst1, lst2):
	l1hash = [hash[0] for hash in lst1] 
	l2hash = [hash[0] for hash in lst2]
	l1loc = {hash[0]:hash[1:] for hash in lst1}
	l2loc = {hash[0]:hash[1:] for hash in lst2}
	
	l3hash = list(set(l1hash)&set(l2hash))
	l3 = [(hash, l1loc[hash], l2loc[hash]) for hash in l3hash] 
	sim = len(l3)/min(len(set(l1hash)), len(set(l2hash)))
	return l3, sim

def similarity(lst1, lst2):
	l1hash = [hash[0] for hash in lst1] 
	l2hash = [hash[0] for hash in lst2]
	l3hash = list(set(l1hash)&set(l2hash))
	sim = len(l3hash)/min(len(set(l1hash)), len(set(l2hash)))
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
		for hash in intersect:
				markings_i += [hash[1][1]]
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
			for hash in intersect:
				markings[i][j] += [hash[1][1]]
				markings[j][i] += [hash[2][1]]				

	return C, markings			