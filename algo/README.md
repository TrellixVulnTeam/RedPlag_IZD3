The main file for detecting plagiarism is similarity.py

How to run it :

python3 similarity.py <folder_name>

It MIGHT work with python3 similarity.py <folder_path>. Please try to test using this format.



What does it do?

Prints correlation matrix on stdout
Makes 2 folders in the folder to be tested - Graphs and CSV
Graphs contains 2 graphs - 
I. Histogram
II. Heat map
CSV file contains the similarities in the format
file_1,file_2,similarity
Some points to be noted on this -
A. Similarity is a number between 0 and 1 (both inclusive in case it is not obvious).
B. Only one of (file_1,file_2,similarity), (file_2,file_1,similarity) will exist in the CSV file.
C. CSV file will not contain (file_1,file_1,similarity) as this is trivial and the similarity will be 1.
D. The similarities are arranged in no order. Use sqlite3 or something to sort according to your requirements.
