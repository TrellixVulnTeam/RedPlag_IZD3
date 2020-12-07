""" \package Word Embedding
Plagiarism detector for text files.
Detects plagiarism using GloVe vectors using a similar approach winnowing algorithm.
"""




import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
from .graph_utils import *
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist
from django.conf import settings

## \var dictionary $word_to_vec
## Glove conversion from word to vector

word_to_vec = {}


def generate_embedding_dict():
        print(os.getcwd())
        with open('files/glove100D.txt', encoding='utf-8') as glove:
                lines = [line for line in glove]
                for line in lines:
                        line = line.split(' ')
                        vec = list(map(float,line[1:]))
                        vec = np.array(vec)
                        word_to_vec[line[0]] = vec


def word_centroid(kgram):
	"""!
	\brief Returns centroid of glove vectors of kgram.
	\details Returns centroid of glove vectors of words in kgram.
	\param kgram : list of words whose centroid is to be computed
	\return centroid : Centroid of glove vectors of all words in kgram.
	"""
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
	"""!
	\brief Calculates centroids of window size k
	\detail Calculates centroids of window size of character k using GloVe word to vec dataset.
	\param filename : Path of file whose hashes or centroids have to be calculated.
	\param k : Size of sliding window.
	\returns H : Hashes of sliding windows
	"""


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
	"""!
	\brief Implementation of winnowing algorithm for vectors.
	\detail Winnowing algorithm implemented for vectors. Criteria : select vector closest to centroid using cosine similarity. If equally close vectors exist, choose the one which is to the right.
	\param H : The hashes of the sliding windows.
	\param t : The threshold size
	\param k : The size of the sliding window.
	\returns HS : Fingerprint of document
	"""	


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
	"""!
	\brief Calculates similarity coefficient between 2 files based on their fingerprint.
	\detail Calculates similarity coefficient between 2 files using their fingerprints X and Y. The similarity is calculated as trace(X'XY'Y) / sqrt(trace((X'X)^2) * trace((Y'Y)^2))
	\param X : Fingerprint of file 1 of dimension n x 100.
	\param Y : Fingerprint of file 2 of dimension m x 100.
	\returns similarity : similarity between file 1 and file 2.
	"""

	M = np.transpose(X).dot(X)
	N = np.transpose(Y).dot(Y)
  
	
	A = M.dot(M)
	B = N.dot(N)

	trace_MN = np.trace(M.dot(N))
	trace_M2 = np.trace(A)
	trace_N2 = np.trace(B)
	if ((trace_M2 == 0) or (trace_N2 == 0)): return 1

	similarity = trace_MN / ((trace_M2 * trace_N2) ** (0.5))
	return similarity

	
def moss_embedding(t1, t2, t, k):
	"""!
	\brief Returns similarity between two files.
	\detail Returns similarity between two files without needing to iterate over all pairs of files.
	\param t1 : Path of file 1
	\param t2 : Path of file 2
	\param t : Threshold length of winnowing algorithm
	\param k : Sliding window length for calculating hash
	\returns s : Similarity between file 1 and file 2
	"""

	H1 = GetEmbeddingHashesCharacter(t1, k)
	H2 = GetEmbeddingHashesCharacter(t2, k)
	HS1 = Winnowing(H1, t, k)
	HS2 = Winnowing(H2, t, k)

	s = similarity_metric_1(np.array(HS1), np.array(HS2))
	return s

def embedding_process_files(zip_dir):
        initial_path = os.getcwd()
        os.chdir(settings.BASE_DIR)
        print(os.getcwd())
        generate_embedding_dict()
        basename = os.path.basename(zip_dir).split('.')[0]
        folder_path = settings.MEDIA_ROOT + '/' + basename + '/'
        other_things = settings.MEDIA_ROOT + '/' + basename + 'other/'

        with zipfile.ZipFile(zip_dir,'r') as zip_ref:
                zip_ref.extractall(folder_path)

        ## \var int $t
        ## Threshold length for winnowing algorithm
        t = 100

        ## \var int $k
        ## Sliding window length
        k = 30

        ## \var list $files
        ## List of files in folder which is being queried

        files = os.listdir(folder_path)
        print(os.getcwd())
        os.chdir(folder_path)
        print(os.getcwd())

        ## \var np.darray $H
        ## Array of hashes of each file

        H = [GetEmbeddingHashesCharacter(f,k) for f in files]

        ## \var np.darray $HS
        ## Array of fingerprints of each file

        HS = [Winnowing(h,t,k) for h in H]

        ## \var int $n
        ## Number of files being queried

        n = len(files)
        ## \var list $paths
        ## List of paths of each file

        paths = []
        for f in files:
                paths.append(folder_path + "/" + f)

        ## \var $dict $num_to_files
        ## Mapping of index of file to file name

        num_to_files = {}

        for i in range(len(files)):
                num_to_files[i] = files[i]

        ## \var np.darray $C1
        ## Similarity matrix between files

        C1 = np.identity(n)

        for i in range(n):
                for j in range(i):
                        s1 = similarity_metric_1(HS[i], HS[j])
                        C1[i][j] = s1
                        C1[j][i] = s1

        histogram(C1,other_things)
        plot_heat_map(C1,files,other_things)
        save_csv_file(C1,num_to_files,other_things)
        
        print(os.getcwd())
        os.chdir(settings.MEDIA_ROOT)
        print(os.getcwd())
        if os.path.isfile(basename + 'other' + '.zip'): os.remove(basename + 'other' + '.zip')
        zipf = zipfile.ZipFile(basename + 'other' + '.zip','w',zipfile.ZIP_DEFLATED)
        zipdir(basename + 'other/', zipf)
        zipf.close()
        print(os.getcwd())
        os.chdir(initial_path)
        os.chdir(settings.BASE_DIR)
        print(os.getcwd())
