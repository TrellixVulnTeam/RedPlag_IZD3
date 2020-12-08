# RedPlag
## CS 251 Project

### What we have implemented so far -  
### Core Logic :

1. English Language :
	- Used GloVe vectors to get meaning of word rather than character of word to detect plagiarism
	- Implemented an algorithm similar to k-gram and winnowing.
	- k-gramming equivalent : Words are selected completely to get the number of characters closest to k as possible. 
	Next word is __always__ chosen in next iteration so that algorithm does not get stuck.
	- Winnowing : Vectors closest to centroid of current window are chosen using cosine similarity. If tie, vector to the right is chosen.
	- Similarity Metric : 
		+ The fingerprints won't be of similar sizes in most cases. 
		+ And vectors in n dimensional spaces are not easily countable on a computer.
		+ So, the metric we defined was - let the fingerprint of file 1 be X (a x n matrix) and the fingerprint of file 2 be Y (b x n) matrix. 
		+ Our similarity metric was trace(XX'YY')/ sqrt(trace((XX')^2) * trace((YY')^2)
2. C++ pro :
	- Blah blah blah
	- xyz
3. Python pro :
	- Blah blah blah
	- xyz
4. Codes in other languages :
	- Tokenized the given code file using `pygments` library where each variable name was replaced by V, function name by F and strings by S
	- While tokenizing, we stored the mapping from final character locations to initial locations
	- Implemented
	- xyz
5. Graphical visualisation :
	- We should really add a surface plot. If not on the frontend, at least return in downloads.
	- xyz

### Backend :
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

### Frontend :

+ Login: Allows a user to Enter login details, which links to dashboard
	+ Sign-Up: Allows a user to create a new account for the Red-Plag website
	+ Header : Contains Red Plag, My Account, Sign Out
	+ Red Plag: Allows user to upload a file, and download the graphs and visualisation
	+ My Account: Created Sidebar, which links to various functionalities for your account, such as viewing details, editing, changing password and deleting account
	+ Build components for login/signup, Dashboard which has these sub components: Header(with router links to other componenets and option of logout), My_account, Red_plag(where file upload and download takes place)
	+ Put Authentication gaurds on each url so that only authenticated user can access them
	+ Build an Auth Interceptor that adds JSON web token in the request header of every subsequent request after login, for authentication purpose at the backend. The token is obtained as a response of the GET request of user login
	+ Created Services for Authentication that handles login, signup and my_account section and File service handles upload and download of data.(upload part is left)

### Bonus Features :
1. Terminal :
	- Login
	- Change Password
	- Upload
	- Download
2. Boilerplate removal :
	- Blah Blah Blah
3. Python Pro :



### What technology we have used -  

+ Python was used for implementing the core logic as well as the backend and following libraries were used - 
	- numpy
	- matplotlib
	- scipy
	- zipfile
+ Angular for the frontend
+ Django and Django REST framework for the backend with JWT authentication 
+ sqlite for backend database
+ SCSS for styling

### How the Website is supposed to be run - 
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

### How the terminal is supposed to be run :

### Usage

The server must be active. If you are testing locally, follow the instructions for the backend.

#### For Ubuntu and Mac users

The name of the terminal file is `redplagcli`. The `redplag_support.py` file must be present in the same folder as `redplagcli`.
First make `redplagcli` executable by using the command `chmod a+x redplagcli`
If this fails, you may use `python3 replag_support.py`

##### Commands

+ Login:
`.\redplagcli login <email_id> <password>`

+ Change Password:
It is necessary to first login before changing password.
`.\redplagcli change <old_password> <new_password>`

+ Upload:
`.\replagcli upload <zip_file_path> <type_of_plag_check>`
	- Optional arguments : `[-b (short) or --boilerplate (long)] <boilerplate_path>`
	- zip file must have all files to be checked at depth 0 only. It must not contain any other subfolders.
	- types of plag check and the argument to be passed :
		1. C++ : cpp
		2. Python : python
		3. Codes in other languages : moss
		4. English Language Text : text

+ Download:
`.\redplagcli download`
	- Optional arguments : `[-p (short) or --path (long)] <download_path>`


#### For Windows Users.

Use the .exe file named `redplag.exe`
If this fails, you may use `python3 redplag_support.py`

##### Commands

+ Login:
`.\redplag.exe login <email_id> <password>`

+ Change Password:
It is necessary to first login before changing password.
`.\redplag.exe change <old_password> <new_password>`

+ Upload:
`.\redplag.exe upload <zip_file_path> <type_of_plag_check>`
	- Optional arguments : `[-b (short) or --boilerplate (long)] <boilerplate_path>`
	- zip file must have all files to be checked at depth 0 only. It must not contain any other subfolders.
	- types of plag check and the argument to be passed :
		1. C++ : cpp
		2. Python : python
		3. Codes in other languages : moss
		4. English Language Text : text

+ Download:
`.\redplag.exe download`
	- Optional arguments : `[-p (short) or --path (long)] <download_path>`

