import re


infile = open('./test_function.cpp')

#detecting functions

L = []
cnt =0;
# trigger = 1
for line in infile:
	# print(cnt)
	if cnt!=0:
		if line.find('}')!=-1:
			line = line.replace('}', '')
			if len(line)!=0 and line!='\n' and line!='\t':
				L[len(L)-1][2].append(line);
			# print("hello")
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
		# print(c)
		if c == 1:
			c=0
			break
		string_new = line[line.find('(')+1:line.find(')')]
		list_new = string_new.split(",")
		for i in range(0,len(list_new)):
			list_new[i] = list_new[i].strip().split(' ');
		# if(fun_name=='main'):
		# 	continue
		L.append([fun_name, list_new, []])
		# print(list_new)
# print(L)
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
# print(main_fun)
for alpha in range(0, 3):
	for item in L:
		# print(item)
		ix = L.index(item)
		line = 0
		while line < len(item[2]):
			for fun in L:
				if recursive_list[L.index(fun)]==1:
					continue
				s = item[2][line]
				# print(s)
				if s.find(fun[0])!=-1 and fun[0]!=item[0]:
					# is_used[L.index(fun)] = 1
					# print(line)
					idx = s.find(fun[0])
					idx2 = s.find(')')
					func = s[idx :idx2+1]
					# print(func)
					var_names = func.split('(')[1].split(')')[0].split(',')
					for i in range(0, len(var_names)):
						var_names[i] = var_names[i].strip()
					# print(var_names)
					# finding data types of variables
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
					# print(var_data_type)
					# print(L)
					# finding the function body that needs to be replaces with the given function
					index_of_function_to_replace = L.index(fun)
					# print(fun)
					for f in L:
						new_l = [x[0] for x in f[1]]
						# print(new_l)
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
					# print(var_names)
					# print(var_data_type)
					# print(idx, idx2)
					# print(index_of_function_to_replace)
					# print(item)
					new_line = L[index_of_function_to_replace][2].copy()
					# print(new_line)
					# print(old_var_names)
					old_var_names = [x[1] for x in L[index_of_function_to_replace][1]]
					# print(old_var_names)
					# print(var_names)
					return_lines = []
					return_indices = []
					for li in new_line:
						# print(li)
						idkx = new_line.index(li)
						if li.find('return')!=-1:
							new_line[idkx] = new_line[idkx].replace('return ', '')
							# return_lines.append(idkx)
							# return_indices.append(li.find('return'))
						for v in old_var_names:
							# print(v)
							# if v=='b':
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
							# print(x)
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
								# print(x)
								y.reverse()
								for match in y:
									# print(match)
									start = li.find(match)
									end = start + len(v)
									# print(li)
									# print(new_line)
									new_line[idkx] = new_line[idkx][:start] + var_names[old_var_names.index(v)] + new_line[idkx][end:]
					for lin in new_line:
						L[ix][2].insert(line, lin)
						line = line + 1
					# line = line+1
					range_list = [(idx, idx2+1)]
					S = L[ix][2][line]
					# print(S)
					res = ''.join(chr for indx, chr in enumerate(S, 1) if not any(strt_idx <= indx <= end_idx for strt_idx, end_idx in range_list)) 
					item[2][line] = res
			line = line + 1
					# print(new_line)

# print(recursive_list)



used_functions = [0 for i in range(0, len(L))]
# replace functions in main and remove the replaced and redundant functions
line = 0
while line<len(main_fun[2]):
	for fun in L:
		if recursive_list[L.index(fun)]==1:
			continue
		s = main_fun[2][line]
		# print(s)
		# print(fun[0])
		# print(s.find(fun[0]))
		if s.find(fun[0])!=-1:
			used_functions[L.index(fun)] = 1
			# print(fun)
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
	# print(line)
	line = line + 1;

# print(used_functions)
for i in range(len(used_functions)-1, -1, -1):
	if used_functions[i]==0 and recursive_list[i]==0:
		L.pop(i)

print(main_fun)
print(L)

