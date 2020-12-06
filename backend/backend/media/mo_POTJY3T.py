import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy

q=1000000007

def GetH(t, k):
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
	H1=GetH(t1,k)
	H2=GetH(t2,k)
	HS1=set(Win(H1,t,k))
	HS2=set(Win(H2,t,k))
	s=len(HS1&HS2)/min(len(HS1),len(HS2))
	return s

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
    file_path = folder_path + "/Graphs/histogram." + img_format
    folder_loc = folder_path + "/Graphs"
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
    
    file_path = folder_path + "/Graphs/heat_map." + img_format
    
    plt.savefig(file_path)
    plt.clf()
            

def save_csv_file(correlation_matrix,num_to_files,folder_path):
    """Saves similarity between files"""

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
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
    paths = []

    for f in files:
        paths.append(folder_path + "/" + f)

    num_files = len(files)
    correlation_matrix = np.identity(num_files)
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
    plot_heat_map(correlation_matrix,folder_path)
    save_csv_file(correlation_matrix,num_to_files,folder_path)


if __name__ == '__main__':
    main()