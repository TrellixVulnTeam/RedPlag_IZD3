# RedPlag
cs251 project



README for algo :

The main file for detecting plagiarism is similarity.py

(install numpy and matplotlib if not installed)

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



### Instructions to run the backend:
1. cd to this ./backend/ (i.e. the folder that contains this readme file)
2. source env/bin/activate    (run this to activate the virtual environment)
3. pip install -r requirements.txt   (Do this for the first time you run the virtual environment to install all the dependencies)
4. Whenever you install a dependency for the backend run: pip freeze > requirements.txt before commiting you work so that others donn't face clashes.
5. To deactivate the virtual environment after your work run: deactivate



# Frontend

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.6.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
