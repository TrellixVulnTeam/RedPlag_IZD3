import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy
import zipfile
from django.conf import settings


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

word_to_vec = {}
with open('glove50D.txt') as glove:
  for line in glove:
    line = line.split(' ')
    vec = list(map(float,line[1:]))
    vec = np.array(vec)
    word_to_vec[line[0]] = vec

def evaluate_centroid(filename):
  centroid = np.zeroes(50)
  with open(filename) as f:
    num_words = 0
    for line in f:
      line = line.split(' ')
      for word in line:
        if word in word_to_vec:
          centroid += word_to_vec[word]
        num_words += 1
    centroid = centroid/num_words

def similarity(f1, f2):
  return np.dot(f1,f2)/(np.sqrt(np.dot(f1,f1))*np.sqrt(np.dot(f2,f2)))

def histogram(correlation_matrix,folder_path,bin_size = 0.10,img_format = 'png'):
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
    file_path = folder_path + "\\Graphs\\histogram." + img_format
    folder_loc = folder_path + "\\Graphs"
    if not os.path.exists(folder_loc):
        os.makedirs(folder_loc)
    
    plt.hist(count, bins = bins)
    plt.xlabel("Similarity")
    plt.ylabel("Frequency of such similarity")
    plt.title("Histogram of frequency of similarity vs similarity")
    plt.xlim([0, 1])

    #plt.show()
    plt.savefig(file_path)
    plt.clf()


def plot_heat_map(correlation_matrix,folder_path,coloring = 'hot', img_format = '.png'):
    """Plots heat map of the correlation matrix. Coloring specifies the colour scheme."""

    plt.imshow(correlation_matrix, cmap = coloring)
    #plt.show()
    if (img_format[0] == '.'):
        img_format = img_format[1:]
    
    file_path = folder_path + "\\Graphs\\heat_map." + img_format
    
    plt.savefig(file_path)
    plt.clf()
            

def save_csv_file(correlation_matrix,num_to_files,folder_path):
    """Saves similarity between files in decreasing order"""

    csv_list = []
    num_files = correlation_matrix.shape[0]

    file_path = folder_path + "\\CSV\\similarity_list.csv"
    folder_loc = folder_path + "\\CSV"

    if not os.path.exists(folder_loc):
        os.makedirs(folder_loc)

    with open(file_path,'w') as fout:
        for i in range(1,num_files):
            for j in range(i):
                line = num_to_files[i] + ',' + num_to_files[j] + ',' + str(correlation_matrix[i][j]) + '\n'
                fout.write(line)


def process_given_files(zip_dir):
    basename = os.path.basename(zip_dir).split('.')[0]
    folder_path = settings.MEDIA_ROOT + '/' + basename + '/'
    other_things = settings.MEDIA_ROOT + '/' + basename + 'other/'
    #out_file_name = settings.MEDIA_ROOT + '/' + basename + '.txt'
    with zipfile.ZipFile(zip_dir,'r') as zip_ref: #zip_dir is the uploaded file name
        zip_ref.extractall(folder_path)   #folder_path can be hardcoded but files must be removed just after processing
    
    files = os.listdir(folder_path)
    centroids = []

    for f in files: centroids.append(evaluate_centroids(folder_path + "/" + f))

    num_files = len(files)
    correlation_matrix = np.identity(num_files)
    num_to_files = {}


    for i in range(len(files)):
        num_to_files[i] = files[i]


    #output_file = open(out_file_name,'w') # Output Matrix be stored here

    for i in range(num_files):
        for j in range(i+1,num_files):
            sim = similarity(centroids[i],centroids[j])
            correlation_matrix[i][j] = sim
            correlation_matrix[j][i] = sim


    """for i in range(num_files):
        for j in range(num_files):
            output_file.write('(' + str(i) + ',' + str(j) + ') : ' + str(correlation_matrix[i][j]) + ' ')
        output_file.write('')"""

    histogram(correlation_matrix,other_things)
    plot_heat_map(correlation_matrix,other_things)
    save_csv_file(correlation_matrix,num_to_files,other_things)

    os.chdir(settings.MEDIA_ROOT)
    if os.path.isfile(basename + 'other' + '.zip'): os.remove(basename + 'other' + '.zip')

    zipf = zipfile.ZipFile(basename + 'other' + '.zip','w',zipfile.ZIP_DEFLATED)
    zipdir(basename + 'other/', zipf)
    zipf.close()

    #output_file.close()
