import os
import re
import sys
import numpy
import matplotlib
import scipy
import zipfile
from django.conf import settings


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
    mu = numpy.mean(vec)
    sigma = numpy.std(vec)
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


    vec_1 = numpy.array(list_1)
    vec_2 = numpy.array(list_2)
    sorted_vec_1 = numpy.sort(vec_1)
    sorted_vec_2 = numpy.sort(vec_2)
    sorted_and_normalised_vec_1 = normalise_vec(sorted_vec_1)
    sorted_and_normalised_vec_2 = normalise_vec(sorted_vec_2)
    #print(vec_1)
    #print(vec_2)
    #print(sorted_and_normalised_vec_1)
    #print(sorted_and_normalised_vec_2)
    #print()
    
    
    #C = numpy.corrcoef(sorted_vec_1,sorted_vec_2)
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

folder_path = '../media/code_running'

def process_given_files(zip_dir):
    zip_dir = '../media/' + zip_dir
    with zipfile.ZipFile(zip_dir,'r') as zip_ref: #zip_dir is the uploaded file name
        zip_ref.extractall(folder_path)   #folder_path can be hardcoded but files must be removed just after processing
    
    files = os.listdir(folder_path)
    word_dict = []

    for f in files: word_dict.append(compute_dict(folder_path + "/" + f))

    num_files = len(files)
    correlation_matrix = numpy.identity(num_files)

    output_file = open('../media/out.txt','w') # Output Matrix be stored here

    for i in range(num_files):
        for j in range(i+1,num_files):
            similarity = correlation_coefficient_padding(word_dict[i],word_dict[j])
            correlation_matrix[i][j] = similarity
            correlation_matrix[j][i] = similarity


    for i in range(num_files):
        for j in range(num_files):
            output_file.write('(' + str(i) + ',' + str(j) + ') : ' + str(correlation_matrix[i][j]) + ' ')
        #print(correlation_matrix[i][j]," ",end="")
        output_file.write('\n')
        #print()


    #for f in files:
     #   os.remove(f)

    output_file.close()

