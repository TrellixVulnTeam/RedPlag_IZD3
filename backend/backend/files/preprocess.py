import re
import sys

def stripcomments(filename):

	infile = open(filename, 'r',  encoding = 'utf-8').read()
	infile = re.sub('//.*?\n|/\*.*?\*/', '', infile, flags=re.S)
	open(filename, 'w').write(infile)


def replace_define(filename):

	infile = open(filename, 'r',  encoding = 'utf-8')
	out = ""
	define = []
	definition = []
	for l in infile:
		for i in range(0, len(define)):
			x = []
			y = []
			j = 0
			while j<len(l):
				match = re.search(r"(\W|\b)(" + define[i] + ")(\W|\b)", l[j:])
				if match!=None:
					x.append(match.group(2))
					y.append(match.start() + j)
					j = j + match.end() - 1
				else:
					break
			x.reverse()
			y.reverse()
			for k in range(0, len(y)):
				start = y[k] + 1
				end = start + len(define[i])
				l = l[:start] + definition[i] + l[end:]
		t = 0
		if l.startswith("#define"):
			items = l.split(' ')
			define.append(items[1].strip())
			definition.append(items[2].strip())
			t = 1
		if t ==0:
			out = out + l

	infile.close()

	outfile = open(filename, 'w',  encoding = 'utf-8')

	outfile.write(out)
	outfile.close()

def replace_function(filename):
	#detecting functions

	infile = open(filename, 'r',  encoding = 'utf-8')

	L = []
	cnt =0;
	for line in infile:
		if cnt!=0:
			if line.find('}')!=-1:
				line = line.replace('}', '')
				if len(line)!=0 and line!='\n' and line!='\t':
					L[len(L)-1][2].append(line);
				cnt = cnt - 1
			else:
				L[len(L)-1][2].append(line);
			continue
		if line.find('{')!=-1:
			cnt = cnt + 1 
		if line.find('(')!=-1 and line.find(')')!=-1:
			if line.find(';')!=-1 and line.find('{')==-1:
				continue
			list = line.split(' ');
			c = 0
			for item in list:
				index = item.find('(')
				index2 = item.find(')')
				if index!=-1:
					if index ==0:
						fun_index = list.index(item)-1
						fun_name = list[fun_index]
						if(fun_index==0):
							c=1
							break
					else:
						fun_index = list.index(item)
						fun_name = list[fun_index][0:index]
						if(fun_index==0):
							c=1
							break
			if c == 1:
				c=0
				break
			string_new = line[line.find('(')+1:line.find(')')]
			list_new = string_new.split(",")
			for i in range(0,len(list_new)):
				list_new[i] = list_new[i].strip().split(' ');
			L.append([fun_name, list_new, []])

	# checking if the function is recursive or not
	recursive_list = []
	for item in L:
		found = 0
		for line in range(0, len(item[2])):
			if item[2][line].find(item[0])!=-1:
				found = 1
				recursive_list.append(1)
				break
		if found == 0:
			recursive_list.append(0)

	#replacing function definition to develop compound definition
	def is_number(s):
	  try:
	    float(s) # for int, long and float
	  except ValueError:
	    try:
	      complex(s) # for complex
	    except ValueError:
	      return False
	  return True

	main_index = -1
	for i in range(0, len(L)):
		if L[i][0]=='main':
			main_index = i
			break

	main_fun = L.pop(main_index)

	for alpha in range(0, 4):
		for item in L:
			ix = L.index(item)
			line = 0
			while line < len(item[2]):
				for fun in L:
					if recursive_list[L.index(fun)]==1:
						continue
					s = item[2][line]
					if s.find(fun[0])!=-1 and fun[0]!=item[0]:
						idx = s.find(fun[0])
						idx2 = s.find(')')
						func = s[idx :idx2+1]
						var_names = func.split('(')[1].split(')')[0].split(',')
						for i in range(0, len(var_names)):
							var_names[i] = var_names[i].strip()
						var_data_type = []
						for var in var_names:
							if is_number(var):
								var_data_type.append('any')
								continue
							elif var.startswith("\'"):
								var_data_type.append('char')
								continue
							elif var.startswith("\""):
								var_data_type.append('string')
								continue
							found = 0
							for line2 in item[2]:
								if found == 1:
									break
								index = max(line2.find(' ' + var + ','), line2.find(' ' + var + ' '), line2.find(' ' + var + ';'), line2.find(',' + var + ' '), line2.find(',' + var + ','), line2.find(',' + var + ';'))
								if index!=-1:
									index2 = [i for i in range(len(line2)) if line2.startswith(';', i)]
									for i in index2:
										if index < i:
											if index2.index(i)==0:
												type = line2[0:i].strip().split(' ')[0]
												var_data_type.append(type)
												found = 1
												break
											else:
												type = line2[index2[index2.index(i)-1]+1:i].strip().split(' ')[0]
												var_data_type.append(type)
												found = 1
												break
						# finding the function body that needs to be replaces with the given function
						index_of_function_to_replace = L.index(fun)

						for f in L:
							new_l = [x[0] for x in f[1]]
							if f[0]==fun[0] and len(new_l)==len(var_data_type):
								match = 1
								for i in range(0, len(new_l)):
									if var_data_type[i]==new_l[i]:
										continue
									elif var_data_type=='any':
										if new_l[i]=='int' or new_l[i]=='double' or new_l=='float':
											continue
										else:
											match = 0
											break
									else:
										match = 0
										break
								if match == 1:
									index_of_function_to_replace = L.index(f)
								

						# replacing the function
						new_line = L[index_of_function_to_replace][2].copy()
						old_var_names = [x[1] for x in L[index_of_function_to_replace][1]]
						return_lines = []
						return_indices = []
						for li in new_line:
							idkx = new_line.index(li)
							if li.find('return')!=-1:
								new_line[idkx] = new_line[idkx].replace('return ', '')
							for v in old_var_names:
								strng = new_line[idkx]
								x = []
								i=0

								while i < len(strng):
									m = re.search(r"\W"+v+r"\W", strng[i:])
									if m!=None:
										x.append(m.group(0))
										i = i+m.start()+1
									else:
										break

								if len(x)!=0:
									x.reverse()
									for match in x:
										start = new_line[idkx].find(match)+1
										end = start + len(v)
										new_line[idkx] = new_line[idkx][:start] + var_names[old_var_names.index(v)] + new_line[idkx][end:]
								y = []
								i=0
								while i < len(strng):
									m = re.search(r"\A"+v+r"\W", strng[i:])
									if m!=None:
										y.append(m.group(0))
										i = i+m.start()+1
									else:
										break
								if len(y)!=0:
									y.reverse()
									for match in y:
										start = li.find(match)
										end = start + len(v)
										new_line[idkx] = new_line[idkx][:start] + var_names[old_var_names.index(v)] + new_line[idkx][end:]
						for lin in new_line:
							L[ix][2].insert(line, lin)
							line = line + 1
						range_list = [(idx, idx2+1)]
						S = L[ix][2][line]
						res = ''.join(chr for indx, chr in enumerate(S, 1) if not any(strt_idx <= indx <= end_idx for strt_idx, end_idx in range_list)) 
						item[2][line] = res
				line = line + 1
	used_functions = [0 for i in range(0, len(L))]

	# replace functions in main and remove the replaced and redundant functions
	line = 0
	while line<len(main_fun[2]):
		for fun in L:
			if recursive_list[L.index(fun)]==1:
				continue
			s = main_fun[2][line]
			if s.find(fun[0])!=-1:
				used_functions[L.index(fun)] = 1
				idx = s.find(fun[0])
				idx2 = s.find(')')
				func = s[idx :idx2+1]
				var_names = func.split('(')[1].split(')')[0].split(',')
				for i in range(0, len(var_names)):
					var_names[i] = var_names[i].strip()
				var_data_type = []
				for var in var_names:
					if is_number(var):
						var_data_type.append('any')
						continue
					elif var.startswith("\'"):
						var_data_type.append('char')
						continue
					elif var.startswith("\""):
						var_data_type.append('string')
						continue
					found = 0
					for line2 in main_fun[2]:
						if found == 1:
							break
						index = max(line2.find(' ' + var + ','), line2.find(' ' + var + ' '), line2.find(' ' + var + ';'), line2.find(',' + var + ' '), line2.find(',' + var + ','), line2.find(',' + var + ';'))
						if index!=-1:
							index2 = [i for i in range(len(line2)) if line2.startswith(';', i)]
							for i in index2:
								if index < i:
									if index2.index(i)==0:
										type = line2[0:i].strip().split(' ')[0]
										var_data_type.append(type)
										found = 1
										break
									else:
										type = line2[index2[index2.index(i)-1]+1:i].strip().split(' ')[0]
										var_data_type.append(type)
										found = 1
										break
				index_of_function_to_replace = L.index(fun)
				for f in L:
					new_l = [x[0] for x in f[1]]
					if f[0]==fun[0] and len(new_l)==len(var_data_type):
						match = 1
						for i in range(0, len(new_l)):
							if var_data_type[i]==new_l[i]:
								continue
							elif var_data_type=='any':
								if new_l[i]=='int' or new_l[i]=='double' or new_l=='float':
									continue
								else:
									match = 0
									break
							else:
								match = 0
								break
						if match == 1:
							index_of_function_to_replace = L.index(f)
				new_line = L[index_of_function_to_replace][2].copy()
				old_var_names = [x[1] for x in L[index_of_function_to_replace][1]]
				return_lines = []
				return_indices = []
				for li in new_line:
					idkx = new_line.index(li)
					if li.find('return')!=-1:
						new_line[idkx] = new_line[idkx].replace('return ', '')
					for v in old_var_names:
						strng = new_line[idkx]
						x = []
						i=0

						while i < len(strng):
							m = re.search(r"\W"+v+r"\W", strng[i:])
							if m!=None:
								x.append(m.group(0))
								i = i+m.start()+1
							else:
								break
						if len(x)!=0:
							x.reverse()
							for match in x:
								start = new_line[idkx].find(match)+1
								end = start + len(v)
								new_line[idkx] = new_line[idkx][:start] + var_names[old_var_names.index(v)] + new_line[idkx][end:]
						y = []
						i=0
						while i < len(strng):
							m = re.search(r"\A"+v+r"\W", strng[i:])
							if m!=None:
								y.append(m.group(0))
								i = i+m.start()+1
							else:
								break
						if len(y)!=0:
							y.reverse()
							for match in y:
								start = li.find(match)
								end = start + len(v)
								new_line[idkx] = new_line[idkx][:start] + var_names[old_var_names.index(v)] + new_line[idkx][end:]
				for lin in new_line:
					main_fun[2].insert(line, lin)
					line = line + 1
				range_list = [(idx, idx2+1)]
				S = main_fun[2][line]
				res = ''.join(chr for indx, chr in enumerate(S, 1) if not any(strt_idx <= indx <= end_idx for strt_idx, end_idx in range_list)) 
				main_fun[2][line] = res
		line = line + 1;

	for i in range(len(used_functions)-1, -1, -1):
		if used_functions[i]==0 and recursive_list[i]==0:
			L.pop(i)

	# writing the changes back to the file
	infile.close()
	outfile = open(filename, 'w')

	func_names = []

	for i in range(0, len(L)):
		func_names.append(L[i][0])
		outfile.write(L[i][0]+'(')
		if len(L[i][1][0])==1:
			L[i][1].pop(0)
		for j in range(0, len(L[i][1])):
			if j != len(L[i][1])-1:
				outfile.write(L[i][1][j][0] +' '+ L[i][1][j][1] + ',')
			else:
				outfile.write(L[i][1][j][0] +' '+ L[i][1][j][1])
		outfile.write(')' + '{\n')
		for j in range(0, len(L[i][2])):
			outfile.write(L[i][2][j])
		outfile.write('}\n')

	if len(main_fun[1][0])==1:
			main_fun[1].pop(0)
	func_names.append('main')
	outfile.write(main_fun[0]+'(')
	for j in range(0, len(main_fun[1])):
		if j != len(main_fun[1])-1:
			outfile.write(main_fun[1][j][0] +' '+ main_fun[1][j][1] + ',')
		else:
			outfile.write(main_fun[1][j][0] +' '+ main_fun[1][j][1])
	outfile.write(')' + '{\n')
	for j in range(0, len(main_fun[2])):
		outfile.write(main_fun[2][j])
	outfile.write('}\n')

	outfile.close()
	return func_names

def stripspaces(filename):

	infile = open(filename, 'r',  encoding = 'utf-8').read()

	infile = re.sub('([^a-zA-Z0-9\s]+)', ' \\1 ', infile)
	infile = re.sub('([\s]+)', ' ', infile)
	open(filename, 'w').write(infile)


# replacing variable names by v

def replace_variables(filename, func_names):
	keywords = [
	"alignas",
	"double",
	"reinterpret_cast",
	"alignof",
	"dynamic_cast",
	"requires",
	"and",
	"else",
	"return",
	"and_eq",
	"enum",
	"short",
	"asm",
	"explicit",
	"signed",
	"atomic_cancel",
	"export",
	"sizeof",
	"atomic_commit",
	"extern",
	"static",
	"atomic_noexcept",
	"false",
	"static_assert",
	"auto",
	"float",
	"static_cast",
	"bitand",
	"for",
	"struct",
	"bitor",
	"friend",
	"switch",
	"bool",
	"goto",
	"synchronized",
	"break",
	"if",
	"template",
	"case",
	"import",
	"this",
	"catch",
	"inline",
	"thread_local",
	"char",
	"int",
	"throw",
	"char16_t",
	"long",
	"true",
	"char32_t",
	"module",
	"try",
	"class",
	"mutable",
	"typedef",
	"compl",
	"namespace",
	"typeid",
	"concept",
	"new",
	"typename",
	"const",
	"noexcept",
	"union",
	"constexpr",
	"not",
	"unsigned",
	"const_cast",
	"not_eq",
	"using",
	"continue",
	"nullptr",
	"virtual",
	"co_await",
	"operator",
	"void",
	"co_return",
	"or",
	"cout",
	'endl',
	"volatile",
	"co_yield",
	"char_t",
	"decltype",
	"private",
	"while",
	"default",
	"protected",
	"xor",
	"delete",
	"public",
	"xor_eq",
	"do",
	"register"]


	infile = open(filename, 'r',  encoding = 'utf-8').read()

	infile_temp = infile
	x = []
	y = []
	i=0
	while i<len(infile):
		m = re.search(r"(\W|\b)([a-zA-Z]+[\w]*)(\W|\b)", infile[i:])
		if m!=None:
			x.append(m.group(2))
			y.append(m.start() + i)
			i = i + m.end() -1
		else:
			break

	var = []
	var_loc = []

	for i in range(0, len(x)):
		if x[i] not in keywords and x[i] not in func_names:
			var.append(x[i])
			var_loc.append(y[i])

	var.reverse()
	var_loc.reverse()
	for i in range(0, len(var)):
		start = var_loc[i] + 1
		end = start + len(var[i])
		infile = infile[:start] + 'v' + infile[end:]

	outfile = open(filename, 'w')
	outfile.write(infile)
	outfile.close()

def boiler(bo, co):
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

			with open(co, "r+",  encoding = 'utf-8') as f:

			    d = f.readlines()
			    f.seek(0)
			    done=False
			    for i in d:
			        if i != line or done==True:
			        	f.write(i)
			        else:
			        	done=True
			    f.truncate()


def preprocess(filename, b=False, bo="none.txt"):
	if b==True:
		boiler(bo,filename)
	stripcomments(filename)
	replace_define(filename)
	func_names = replace_function(filename)
	stripspaces(filename)
	replace_variables(filename, func_names)

