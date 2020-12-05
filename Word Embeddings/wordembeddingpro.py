import numpy as np
import os
from scipy.spatial.distance import squareform, pdist

word_to_vec = {}
with open('glove50D.txt', encoding='utf-8') as glove:
	lines = [line for line in glove]
	for line in lines:
		line = line.split(' ')
		vec = list(map(float,line[1:]))
		vec = np.array(vec)
		word_to_vec[line[0]] = vec


def paragraph_centroid(paragraph):
	num_words = 0
	centroid = np.zeros(50)
	for line in paragraph:
		words = line.split(' ')
		for word in words:
			if word in word_to_vec: centroid += word_to_vec[word]
			else: centroid += np.ones(50)
			num_words += 1
	centroid = centroid/num_words
	return centroid

"""def line_centroid(line, k):
        centroid = np.zeros(50)
        for w in line:
                if w in word_to_vec: centroid += word_to_vec[w]
                else: centroid += np.ones(50)
        centroid = centroid/k
        return centroid"""

def GetEmbeddingHashes(filename, k):
	H = []
	with open(filename, encoding='utf-8') as f:
		#lines = f.read()
		#lines = lines.rstrip('\n')
		lines = [line for line in f]
		for i in range(len(lines)-k):
			kparagraph = lines[i:i+k]
			H.append(paragraph_centroid(kparagraph))
	return H

def Winnowing(H, t, k):
	HS = []
	w = t + 1 - k
	n = len(H)

	mean = np.zeros(50)
	for h in H: mean += h
	mean = mean/n

	mI = -1
	pmI = -1

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
	"""X is a numpy matrix of size m x 50. Y is a numpy matrix of size n x 50. This function returns a similarity coefficient between them = trace(X'XY'Y)/sqrt(trace((X'X)^2)trace((Y'Y)^2))."""
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

"""def centered_matrix(X):
	Computes pairwise euclidean distance between rows of X and centers each cell

	M = squareform(pdist(X))
	row_mean = M.mean(axis = 1)
	column_mean = M.mean(axis = 0)
	total_mean = row_mean.mean()

	R = np.tile(row_mean, (M.shape[0],1)).transpose()
	C = np.tile(column_mean, (M.shape[1],1))
	G = np.tile(total_mean,M.shape)

	centered_matrix = M - R - C + G
	return centered_matrix

def similarity_metric_2(X,Y):
	X is a numpy matrix of size m x 50. Y is a numpy matrix of size n x 50. This function returns dCov coefficient.

	X = np.transpose(X)
	Y = np.transpose(Y)

	# Now X and Y have same number of rows
	# X has dimension = 50 x m. Y has dimension = 50 x n

	M = centered_matrix(X)
	N = centered_matrix(Y)

	cov_MN = np.sqrt(M.dot(N).sum())/M.shape[0]
	cov_M = np.sqrt((M.dot(M).sum())/((M.shape[0]) ** (0.5)))
	cov_N = np.sqrt((N.dot(N).sum())/((N.shape[0]) ** (0.5)))

	if ((cov_M > 0.0) and (cov_N > 0.0)): return (cov_MN/np.sqrt(cov_M * cov_N))
	else: return 1"""
	
def moss_embedding(t1, t2, t, k):
	H1 = GetEmbeddingHashes(t1, k)
	H2 = GetEmbeddingHashes(t2, k)
	HS1 = Winnowing(H1, t, k)
	HS2 = Winnowing(H2, t, k)

	s = similarity_metric_1(np.array(HS1), np.array(HS2))
	#r = similarity_metric_2(np.array(HS1), np.array(HS2))
	return s

print(moss_embedding('miraculous.txt','c.txt',9,6))

folder_path = './Cartoons'

t = 9
k = 6

files = os.listdir(folder_path)
os.chdir(folder_path)
H = [GetEmbeddingHashes(f,k) for f in files]
HS = [Winnowing(h,t,k) for h in H]

n = len(files)
C1 = np.identity(n)
#C2 = np.identity(n)

for i in range(n):
	for j in range(n):
		s1 = similarity_metric_1(HS[i], HS[j])
		#s2 = similarity_metric_2(HS[i], HS[j])
		
		C1[i][j] = s1
		C1[j][i] = s1
		
		#C2[i][j] = s2
		#C2[i][j] = s2

print(C1)
#print(C2)
