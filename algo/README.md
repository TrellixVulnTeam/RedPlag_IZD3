The main file for detecting plagiarism is similarity.py

## How to run it :

python3 similarity.py <folder_path>

## What does it do?

Prints correlation matrix on stdout  
Makes 2 folders in the folder to be tested - Graphs and CSV  
Graphs contains 2 graphs -  
	+ Histogram  
	+ Heat map  

CSV file contains the similarities in the format  
file_1,file_2,similarity  

Some points to be noted on this -  
	1. Similarity is a number between 0 and 1 (both inclusive in case it is not obvious).  
	2. Only one of (file_1,file_2,similarity), (file_2,file_1,similarity) will exist in the CSV file.  
	3. CSV file will not contain (file_1,file_1,similarity) as this is trivial and the similarity will be 1.  
	4. The similarities are arranged in no order. Use sqlite3 or something to sort according to your requirements.  