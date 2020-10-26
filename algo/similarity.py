import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy


def compute_dict(file_path):
    """Computes the dict for a file whose path is file_path"""
    file_dict = {}
    with open(file_path) as fin:
        for line in fin:
            line = line.strip()
            txt = re.sub('([^a-zA-Z0-9\s]+)',' \\1 ',line)
            txt = re.sub('([\s]+)',' ',txt)
            words = txt.split(" ")
            for word in words:
                w = str(word)
                if(w not in file_dict):
                    file_dict[w] = 1
                else:
                    file_dict[w] = file_dict[w] + 1
    return file_dict




def normalise_vec(vec):
    """Normalises vector by subtracting mean and dividing by sigma each term"""
    mu = np.mean(vec)
    sigma = np.std(vec)
    return ((vec - mu) / sigma)


def correlation_coefficient_padding(word_dict_1,word_dict_2):
    """Computes the correlation coefficient by the vector and padding method"""
    list_1 = []
    list_2 = []

    for key in word_dict_1:
        if (key in word_dict_2):
            list_1.append(word_dict_1[key])
            list_2.append(word_dict_2[key])
        else:
            list_1.append(word_dict_1[key])
            list_2.append(0)

    for key in word_dict_2:
        if (key not in word_dict_1):
            list_1.append(0)
            list_2.append(word_dict_2[key])


    vec_1 = np.array(list_1)
    vec_2 = np.array(list_2)
    sorted_vec_1 = np.sort(vec_1)
    sorted_vec_2 = np.sort(vec_2)
    sorted_and_normalised_vec_1 = normalise_vec(sorted_vec_1)
    sorted_and_normalised_vec_2 = normalise_vec(sorted_vec_2)
    #print(vec_1)
    #print(vec_2)
    #print(sorted_and_normalised_vec_1)
    #print(sorted_and_normalised_vec_2)
    #print()
    
    
    #C = np.corrcoef(sorted_vec_1,sorted_vec_2)
    #return C[0][1]
    E_X_Y = 0
    E_X_2 = 0
    E_Y_2 = 0
    for i in range(len(sorted_and_normalised_vec_1)):
        E_X_Y = E_X_Y + (sorted_and_normalised_vec_1[i] * sorted_and_normalised_vec_2[i])
        E_X_2 = E_X_2 + (sorted_and_normalised_vec_1[i] * sorted_and_normalised_vec_1[i])
        E_Y_2 = E_Y_2 + (sorted_and_normalised_vec_2[i] * sorted_and_normalised_vec_2[i])

    C = E_X_Y / ((E_X_2 * E_Y_2) ** (0.5))
    return C

def histogram(correlation_matrix,bin_size = 0.10,img_format = 'png'):
    """Counts number of files present in each bin. 1/bin_size must be an integer. 0 < bin_size <= 1. Default value of bin_size is 0.10"""

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
    file_path = os.getcwd() + "\\Graphs\\histogram." + img_format
    if not os.path.exists("Graphs"):
        os.makedirs("Graphs")
    
    plt.hist(count, bins = bins)
    plt.xlabel("Similarity")
    plt.ylabel("Frequency of such similarity")
    plt.title("Histogram of frequency of similarity vs similarity")
    plt.xlim([0, 1])

    #plt.show()
    plt.savefig(file_path)
    plt.clf()


def plot_heat_map(correlation_matrix, coloring = 'hot', img_format = '.png'):
    """Plots heat map of the correlation matrix. Coloring specifies the colour scheme."""

    plt.imshow(correlation_matrix, cmap = coloring)
    #plt.show()
    if (img_format[0] == '.'):
        img_format = img_format[1:]
    
    file_path = os.getcwd() + "\\Graphs\\heat_map" + img_format
    plt.savefig(file_path)
    plt.clf()
            

folder_path = sys.argv[1]
files = os.listdir(folder_path)
word_dict = []

for f in files:
    word_dict.append(compute_dict(folder_path + "/" + f))




num_files = len(files)
correlation_matrix = np.identity(num_files)
files_to_num = {}


for i in range(len(files)):
    files_to_num[files[i]] = i

for i in range(num_files):
    for j in range(i+1,num_files):
        similarity = correlation_coefficient_padding(word_dict[i],word_dict[j])
        correlation_matrix[i][j] = similarity
        correlation_matrix[j][i] = similarity


for i in range(num_files):
    for j in range(num_files):
        print(correlation_matrix[i][j]," ",end="")
    print()

histogram(correlation_matrix)
plot_heat_map(correlation_matrix)
