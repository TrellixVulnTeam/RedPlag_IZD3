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

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
