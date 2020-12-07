""" \package Boilerplate
Removes a given boilerplate from a given textfile
"""

def Edit(bo, co):
	"""!
    \brief Removes the boilerplate from the textfile
    \detail Finds the lines of the boilerplate and deletes them from the textfile. Keeps the function declarations intact.
    \param bo : path to the boilerplate textfile.
    \param co : path to the code textfile
    \returns void
    """ 
	infile = open(bo)

	ct=0;
	s1=["void","int","bool","char","float","double","long"]
	for line in infile :
		skip=False
		if line.find('(')!=-1 and line.find(';')==-1:
			if line.find('{')!=-1:
				ct=ct+1
			if line.find('for')==-1 and line.find('while')==-1:
				skip=True
		elif line.find('{')!=-1:
			ct=ct+1
			if(ct==1):
				skip=True
		elif line.find('}')!=-1:
			ct=ct-1
			if ct==0:
				skip=True
		if skip==False:
			with open(co, "r+") as f:
			    d = f.readlines()
			    f.seek(0)
			    done=False
			    for i in d:
			        if i != line or done==True:
			        	f.write(i)
			        else:
			        	done=True
			    f.truncate()