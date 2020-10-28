# RedPlag
## CS 251 Project

### What we have implemented so far -  

1. Core Logic -  
	+ Implemented the naive algorithm
	+ Added white space insensitivity
	+ Read up some theories for plagiarism detection
2. Backend -
	+ Two models for files -
		- `UploadFile` : for the uploaded zip file
		- `OutputFile` : for the generated zip file of results and has a `ForeignKey` to `UploadFile`
	+ Two views -
		- `FileView` : contains a `post` function for uploading input zip file. Input zip file contains all the files that need to be checked for plagiarism
		- `GraphView` : 
	+ Zip file uploading which contains all the files that need to be checked for plagiarism via `post` function of `FileView`
	+ Extraction of the files and running above algorithm on them to generate CSV file of pairwise similarity, a heat map that shows the covariance matrix pictorially and a histogram that shows the number of pairs in each similarity interval.
	+ Zipping above results and downloading them via `get`function of `GraphView`
3. Frontend - 
	+ Blah


### What technology we have used -  

+ Python for the core logic  
Modules used in Python - 
	- numpy
	- matplotlib
	- scipy
	- os
	- sys
	- re
+ Angular for the frontend
+ Django and Djangorest for the backend
+ CSS for styling

### How the tool is supposed to be run -  

### What is yet to be done -  

1. Core Logic -  
	+ Reading up on more theory
	+ Implementing more improvements
2. Backend -  
	+ Blah Blah
3. Frontend -  
	+ 
