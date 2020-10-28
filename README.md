# RedPlag
## CS 251 Project

### What we have implemented so far -  

1. Core Logic -  
	+ Implemented the counting, padding, sorting and cosine similarity algorithm
	+ Added white space insensitivity
	+ Read up some theories such as hashing and comparing for plagiarism detection
	+ Generated Heat maps, histogram and csv file for simlarity comparision
2. Backend -
	+ Implemented login/signup using JWT(JSON Web Token) authentication with Self defined User models
	+ Imparted one to one relationship between profile data of user and user model
	+ Allow User to view profile, edit profile, change password and delete his account from the My account section
	+ Implemented deleting of token from local storage upon logout
	+ Two models for files -
		- `UploadFile` : for the uploaded zip file
		- `OutputFile` : for the generated zip file of results and has a `ForeignKey` to `UploadFile`
	+ Two views -
		- `FileView` : contains a `post` function for uploading input zip file containing all the files that need to be checked for plagiarism
		- `GraphView` : contains a `get` function that runs the core logic from plag_detect.py file and returns in a zipped form the results and its various visualisations.
	+ Associated each of these to User models by foreign key and allowed only authenticated users to access data from them by the help of permission classes
	+ Extraction of the files and running above algorithm on them to generate CSV file of pairwise similarity, a heat map that shows the covariance matrix pictorially and a histogram that shows the number of pairs in each similarity interval.
	+ Zipping above results and downloading them via `get`function of `GraphView`
3. Frontend - 
	+ Login: Allows a user to Enter login details, which links to dashboard
	+ Sign-Up: Allows a user to create a new account for the Red-Plag website
	+ Header : Contains Red Plag, My Account, Sign Out
	+ Red Plag: Allows user to upload a file, and download the graphs and visualisation
	+ My Account: Created Sidebar, which links to various functionalities for your account, such as viewing details, editing, changing password and deleting account
	+ Build components for login/signup, Dashboard which has these sub components: Header(with router links to other componenets and option of logout), My_account, Red_plag(where file upload and download takes place)
	+ Put Authentication gaurds on each url so that only authenticated user can access them
	+ Build an Auth Interceptor that adds JSON web token in the request header of every subsequent request after login, for authentication purpose at the backend. The token is obtained as a response of the GET request of user login
	+ Created Services for Authentication that handles login, signup and my_account section and File service handles upload and download of data.(upload part is left)


### What technology we have used -  

+ Python was used for implementing the core logic as well as the backend and following libraries were used - 
	- numpy
	- matplotlib
	- scipy
	- zipfile
+ Angular for the frontend
+ Django and Django REST framework for the backend with JWT authentication 
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
	+ Blacklisting of Token at the backend when the user logs out so that he can't use that for logging in again before expiration time as removing token from local storage of the browser doesn't guarantee this
	+ Implementing the concept of token refresh, in which the token is refreshed everytime user makes request from the server before expiration time so that session time can be extended. This feature is good for the security purposes.
3. Frontend -  
	+ Implement the upload file service in the frontend
	+ Adding visualisations and graphs on the website

