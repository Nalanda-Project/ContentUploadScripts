


import os
import sys
from config import content_path
from subprocess import call

file_list = os.listdir(content_path)


print(file_list)

def replace_space(filename):
	return filename.replace(' ','\ ')

def convert_wmvfile(filename):
	filename2 = filename.replace('.wmv','.mp4')
	print(filename2)

	command = "ffmpeg -i "+replace_space(filename)+" "+replace_space(filename2)+" -hide_banner"
	print(command)
	os.system(command)
	os.remove(filename)
	print("**Deleted ",filename)


def convert_docx_pptfile(filename):
	command = "unoconv -f pdf "+replace_space(filename)
	print(command)
	os.system(command)
	os.remove(filename)
	print("**Deleted ",filename)


def conversion_call(filename):
	if filename.endswith('.wmv'):
		convert_wmvfile(filename)

	elif filename.endswith('.docx') or filename.endswith('.pptx'):
		convert_docx_pptfile(filename)


for file in os.listdir(content_path):
	path = content_path +"/"+ file
	for file1 in os.listdir(path):
		path2 = path+"/"+file1
		if os.path.isdir(path2):
			for file2 in os.listdir(path2):
				path3 = path2+"/"+file2
				conversion_call(path3)

		else:
			conversion_call(path2)

print("Converted")