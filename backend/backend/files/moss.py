""" \package Moss Implementation
Plagiarism detector for computer languages.
Detects plagiarism using Fingerprints created by Winnowing after Rabin-Karp Hashing.
"""
import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy
import zipfile
import seaborn as sns
from .graph_utils import *
import files.preprocess as cpp
import files.pyprocess as py
from django.conf import settings

q=1000000007

def GetH(t, k):
    """!
    \brief Calculates the Hashes of k-grams of Textfile t
    \detail Calculates the Hashes of k-grams of Textfile t, using tha Rabin-Karp algorithm
    \param t : Path of file whose hashes have to be calculated.
    \param k : Size of k-grams.
    \returns H : List of Hashes for the textfile
    """
    H=[]
    infile = open(t,'r', encoding = 'utf-8').read()
    infile=infile.rstrip("\n")
    for i in range(0,len(infile)-k):
        kgram=infile[i:i+k]
        h=0
        for j in kgram:
            h=(256*h+ord(j))%q; 
        H.append(h)
    return H

def Win(H,t,k):
    """!
    \brief Implementation of winnowing algorithm for vectors.
    \detail Winnowing algorithm implemented for vectors.
    \param H : The hashes of the textfile.
    \param t : The threshold size
    \param k : The size of k-grams.
    \returns HS : Fingerprint of document
    """ 
    HS=[]
    w=t+1-k
    n=len(H)
    mI=-1
    pmI=-1
    if len(H) < w: HS.append(H[0])
    for i in range(0,len(H)-w+1):
        tm=9223372036854775807
        for j in range(i, i+w):
            if H[j]<=tm:
                mI=j
                tm=H[j]
        if mI != pmI:
            pmI=mI
            HS.append(H[mI])
    return HS

def moss(t1,t2,t,k):
    """!
    \brief Gives the Similiarity coefficient between two textfiles.
    \details Gives the Similarity Coefficient by taking ratio of size of intersection of the Fingerprints and the minimum size between the two Fingerprints
    \param t1 : Path of file 1
    \param t2 : Path of file 2
    \param t : The threshold size
    \param k : The size of k-grams.
    \returns s : similarity between file 1 and file 2.
    """
    H1=GetH(t1,k)
    H2=GetH(t2,k)
    HS1=set(Win(H1,t,k))
    HS2=set(Win(H2,t,k))
    s=len(HS1&HS2)/min(len(HS1),len(HS2))
    return s

def moss_given_files(zip_dir, boilerplate, blank_stub, which_pro):
    initial_path = os.getcwd()
    print(os.getcwd())
    os.chdir(settings.BASE_DIR)
    basename = os.path.basename(zip_dir).split('.')[0]
    folder_path = settings.MEDIA_ROOT + '/' + basename + '/'
    other_things = settings.MEDIA_ROOT + '/' + basename + 'other/'

    with zipfile.ZipFile(zip_dir,'r') as zip_ref: 
        zip_ref.extractall(folder_path)

    ## \var list $files
    ## List of files in folder which is being queried

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]

    ## \var list $paths
    ## List of paths of each file

    paths = []

    for f in files:
        if which_pro == 1: cpp.preprocess(folder_path + "/" + f, not(blank_stub), boilerplate)
        elif which_pro == 2: py.preprocess(folder_path + "/" + f, not(blank_stub), boilerplate)
        paths.append(folder_path + "/" + f)

    num_files = len(files)

    ## \var np.darray $correlation_matrix
    ## Similarity matrix between files
    correlation_matrix = np.identity(num_files)

    ## \var $dict $num_to_files
    ## Mapping of index of file to file name
    num_to_files = {}


    for i in range(len(files)):
        num_to_files[i] = files[i]

    for i in range(num_files):
        for j in range(i+1,num_files):
            similarity = moss(paths[i],paths[j],10,5)
            correlation_matrix[i][j] = similarity
            correlation_matrix[j][i] = similarity


    for i in range(num_files):
        for j in range(num_files):
            print(correlation_matrix[i][j]," ",end="")
        print()


    histogram(correlation_matrix,other_things)
    plot_heat_map(correlation_matrix,files,other_things)
    save_csv_file(correlation_matrix,num_to_files,other_things)

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
