# RedPlag
## CS 251 Project

### What we have implemented so far -  

1. Core Logic -  
	+ Implemented the counting, padding, sorting and cosine similarity algorithm
	+ Added white space insensitivity
	+ Read up some theories such as hashing and comparing for plagiarism detection
2. Backend -
	+ Two models for files -
		- `UploadFile` : for the uploaded zip file
		- `OutputFile` : for the generated zip file of results and has a `ForeignKey` to `UploadFile`
	+ Two views -
		- `FileView` : contains a `post` function for uploading input zip file containing all the files that need to be checked for plagiarism
		- `GraphView` : contains a `get` function that runs the core logic from plag_detect.py file and returns in a zipped form the results and its various visualisations.
	+ Extraction of the files and running above algorithm on them to generate CSV file of pairwise similarity, a heat map that shows the covariance matrix pictorially and a histogram that shows the number of pairs in each similarity interval.
	+ Zipping above results and downloading them via `get`function of `GraphView`
3. Frontend - 
	+ 


### What technology we have used -  

+ Modules used in Python - 
	- numpy
	- matplotlib
	- scipy
	- zipfile
+ Angular for the frontend
+ Django and Django REST framework for the backend
+ SCSS for styling

### How the tool is supposed to be run - 
+ Fire a terminal and `cd` into `backend` directory. 
	- Here run `source env/bin/activate` to enter the virtual environment. 
	- Then run `pip install -r requirements.txt` to install required packages of python
	- `cd` into `backend` directory and run `python3 manage.py runserver` to setup the server
+ Fire another terminal and `cd` into `frontend` directory.
	- Here run `npm install` to install dependencies
	- Then run `ng serve --open` to open the web page after compiling front end application.
+ On the home page, register as a user or login
+ In the RED PLAG tab on top right corner go and upload zip file and download results.
+ In the MY ACCOUNT tab you can view/edit account details


### What is yet to be done -  

1. Core Logic -  
	+ Reading up on more theory
	+ Implementing more improvements
2. Backend -  
	+ Blah Blah
3. Frontend -  
	+ 
