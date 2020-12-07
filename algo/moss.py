""" \package Moss Implementation
Plagiarism detector for computer languages.
Detects plagiarism using Fingerprints created by Winnowing after Rabin-Karp Hashing.
"""


import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns

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
    infile = open(t,'r').read()
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

def histogram(correlation_matrix,folder_path,bin_size = 0.10,img_format = 'png'):
    """!
    \brief Creates histogram of frequencies of values in correlation matrix.
    \details Counts number of files present in each bin. 1/bin_size must be an integer. 0 < bin_size <= 1. Default value of bin_size is 0.10
    \param correlation matrix : Similarity values between all pairs of files
    \param folder_path : Location where graph is to be stored
    \param bin_size : Bin size of histogram. Default value is 0.10
    \param img_format : Format in which image is to be stored. Default value is 'png'
    \return void
    """

    num_files = correlation_matrix.shape[0]
    bins = np.arange(0,1+bin_size,bin_size)
    num_bins = int(1/bin_size)
    total_measurements = int((num_files * (num_files - 1))/2)
    count = np.zeros([total_measurements])
    
    counter = 0
    for i in range(1,num_files):
        for j in range(i):
            count[counter] = correlation_matrix[i][j]
            counter += 1
            
    if(img_format[0] == '.'):
        img_format = img_format[1:]
    file_path = folder_path + "/Graphs/histogram." + img_format
    folder_loc = folder_path + "/Graphs"
    if not os.path.exists(folder_loc):
        os.makedirs(folder_loc)
    
    plt.hist(count, bins = bins)
    plt.xlabel("Similarity")
    plt.ylabel("Frequency of such similarity")
    plt.title("Histogram of frequency of similarity vs similarity")
    plt.xlim([0, 1])

    plt.savefig(file_path)
    plt.clf()


def plot_heat_map(correlation_matrix,files,folder_path,coloring = 'hot', img_format = '.png'):
    """!
    \brief Creates heat map of similarity values of files
    \details Creates heat map of similarity values of files. X - axis and Y - axis represent the files. The colour of the block represents the similarity.
    \param correlation matrix : Similarity values between all pairs of files
    \param files :  List containing names of all files on which plagiarism detection is to be done
    \param folder_path : Location where graph is to be stored
    \param coloring : Coloring of heat map. Default is hot
    \param img_format : Format in which image is to be stored. Default value is 'png'
    \return void
    """

    plt.figure()
    sns.set(font_scale=0.7)
    hm = sns.heatmap(correlation_matrix,
                     cbar=True,
                     annot=True,
                     square=True,
                     fmt='.3f',
                     annot_kws={'size': 12},
                     yticklabels=files,
                     xticklabels=files)
    plt.title('Similarity matrix showing similarity coefficients')
    plt.tight_layout()
    if (img_format[0] == '.'):
        img_format = img_format[1:]
    file_path = folder_path + "/Graphs/heat_map." + img_format
    
    plt.savefig(file_path)
    plt.clf()
            

def save_csv_file(correlation_matrix,num_to_files,folder_path):
    """!
    \brief Stores similarity values between files in a file.
    \details Stores similarity values between files currently stored in correlation_matrix in .csv format
    \param correlation matrix : Similarity values between all pairs of files
    \param num_to_files : Conversion of file index to file name
    \param folder_path : Location where graph is to be stored
    \return void
    """

    csv_list = []
    num_files = correlation_matrix.shape[0]

    file_path = folder_path + "/CSV/similarity_list.csv"
    folder_loc = folder_path + "/CSV"

    if not os.path.exists(folder_loc):
        os.makedirs(folder_loc)

    with open(file_path,'w') as fout:
        for i in range(1,num_files):
            for j in range(i):
                line = num_to_files[i] + ',' + num_to_files[j] + ',' + str(correlation_matrix[i][j]) + '\n'
                fout.write(line)


def main():

    folder_path = sys.argv[1]

    ## \var list $files
    ## List of files in folder which is being queried

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]

    ## \var list $paths
    ## List of paths of each file

    paths = []

    for f in files:
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

    histogram(correlation_matrix,folder_path)
    plot_heat_map(correlation_matrix,files,folder_path)
    save_csv_file(correlation_matrix,num_to_files,folder_path)


if __name__ == '__main__':
    main()