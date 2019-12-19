import os
from config import file_path

fname = []
for root,d_names,f_names in os.walk(file_path):
	for f in f_names:
		fname.append( f)

print(fname)
print(len(set(fname)))
