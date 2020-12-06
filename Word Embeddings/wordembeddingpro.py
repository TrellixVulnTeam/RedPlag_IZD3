import re
import sys
import numpy as np
from numpy.linalg import norm
import os
from scipy.spatial.distance import squareform, pdist

word_to_vec = {}

# Loading glove vectors 

with open('glove100D.txt', encoding='utf-8') as glove:
	lines = [line for line in glove]
	for line in lines:
		line = line.split(' ')
		vec = list(map(float,line[1:]))
		vec = np.array(vec)
		word_to_vec[line[0]] = vec


def word_centroid(kgram):
	"""Returns centroid of kgram using glove vectors. kgram is a list of words."""
	num_words = 0
	centroid = np.zeros(100)
	for word in kgram:
		if word in word_to_vec:
			centroid += word_to_vec[word]
		else: centroid += np.zeros(100)
		num_words += 1
	centroid = centroid/num_words
	if norm(centroid == 0.0):
		return (np.ones(100) / num_words)
	return centroid

def GetEmbeddingHashesCharacter(filename,k):
	"""Returns Hashes of k-grams. k-grams has the number of words such that length (number of characters) is just greater than k. Hash of a k-gram is defined to be the centroid of the glove vectors of the words."""
	H = []
	with open(filename, encoding = 'utf-8') as f:
		lines = [line for line in f]
		words = []
		for line in lines:
			text = re.sub('([^a-zA-Z0-9\s]+)',' ',line)
			text = text.strip()
			text = text.lower()
			text = re.sub('([\s])+',' ',text)
			text = re.sub('(\n+)','',text)
			text = text.strip()
			new_words = text.split(' ')
			for word in new_words:
				words.append(word)
		#print(words[0])
		kgram = []
		i = 0
		length = 0
		n = len(words)
		while length < k and i < n:
			kgram.append(words[i])
			length += len(words[i])
			i += 1


		if (length > k) and (i > 1):
			kgram = kgram[:-1]
			i -= 1
			length -= len(words[i])

		j = 0
		
		H = []
		#print(kgram)
		while i < n:
			H.append(word_centroid(kgram))
			kgram.append(words[i])
			length += len(words[i])
			i += 1

			while length >= k and j < i:
				kgram = kgram[1:]
				length -= len(words[j])
				j += 1

			while length < k and i < n:
				kgram.append(words[i])
				length += len(words[i])
				i += 1

			if length > k and i > (j+1):
				kgram = kgram[:-1]
				i -= 1
				length -= len(words[i])

	if(len(H) == 0):
		return [word_centroid(kgram)]
	
	return H	
		


def Winnowing(H, t, k):
	"""Appplying winnowing algorithm on hashes."""
	HS = []
	w = t + 1 - k
	n = len(H)

	mean = np.zeros(100)
	for h in H: mean += h
	mean = mean/n

	mI = -1
	pmI = -1

	if len(H) < w: HS.append(H[0])
	for i in range(len(H)-w+1):
		tm = 2
		for j in range(i, i+w):
			dot = np.dot(H[j], mean)/np.sqrt(np.dot(H[j],H[j])*np.dot(mean,mean))
			if dot <= tm:
				mI = j
				tm = dot
		if mI != pmI:
			pmI = mI
			HS.append(H[mI])
	return HS
		
def similarity_metric_1(X,Y):
	"""X is a numpy matrix of size m x 100. Y is a numpy matrix of size n x 100. This function returns a similarity coefficient between them = trace(X'XY'Y)/sqrt(trace((X'X)^2)trace((Y'Y)^2))."""
	M = np.transpose(X).dot(X)
	N = np.transpose(Y).dot(Y)
  
	# M is now 50 x 50 matrix
	# N is now 50 x 50 matrix

	A = M.dot(M)
	B = N.dot(N)

	trace_MN = np.trace(M.dot(N))
	trace_M2 = np.trace(A)
	trace_N2 = np.trace(B)
	if ((trace_M2 == 0) or (trace_N2 == 0)): return 1

	similarity = trace_MN / ((trace_M2 * trace_N2) ** (0.5))
	return similarity

	
def moss_embedding(t1, t2, t, k):
	"""Get similarity between t1 and t2."""
	H1 = GetEmbeddingHashesCharacter(t1, k)
	H2 = GetEmbeddingHashesCharacter(t2, k)
	HS1 = Winnowing(H1, t, k)
	HS2 = Winnowing(H2, t, k)

	s = similarity_metric_1(np.array(HS1), np.array(HS2))
	return s


folder_path = sys.argv[1]

t = 100
k = 30


files = os.listdir(folder_path)
os.chdir(folder_path)
H = [GetEmbeddingHashesCharacter(f,k) for f in files]
HS = [Winnowing(h,t,k) for h in H]

n = len(files)

# Similarity matrix
C1 = np.identity(n)

for i in range(n):
	for j in range(i):
		s1 = similarity_metric_1(HS[i], HS[j])
		
		C1[i][j] = s1
		C1[j][i] = s1

print(C1)