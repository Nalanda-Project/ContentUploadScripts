
from enum import Enum
import sys
import json
from os.path import join
import re
from urllib.request import urlopen, HTTPError
# from ricecooker.chefs import SushiChef
# from ricecooker.classes import nodes, questions, files
# from ricecooker.classes.licenses import get_license
# from ricecooker.classes.files import VideoFile, HTMLZipFile, DocumentFile, YouTubeVideoFile
# from ricecooker.exceptions import UnknownContentKindError, UnknownFileTypeError, UnknownQuestionTypeError, raise_for_invalid_channel
# from le_utils.constants import content_kinds,file_formats, format_presets, licenses, exercises, languages
# from pressurecooker.encodings import get_base64_encoding
# import youtube_dl
import pprint
from pathlib import Path
import os 
import pandas as pd
import itertools
from shutil import copyfile
from collections import OrderedDict
from operator import itemgetter
from itertools import groupby
from natsort import natsorted

def downloader(id,p,title):
	'''
    Used to Download the Youtube Videos using command-line program Youtube-dl 
	'''

    # path = "/home/nalanda/Documents/video/"+id+".mp4"
    # os.chdir(p)
    path = p+"/"+title+".mp4"
    # my_file = Path(path)
    print(path)
    if os.path.isfile(path):
    	# pass
        print("Already Downloaded::", path)
    else:
        video_url = 'https://www.youtube.com/watch?v=' + id
        #video_url = 'https://youtu.be/'+id
        os.system('youtube-dl ' +video_url+' --output '+(title+'.mp4').replace(' ','\ '))

        # name = title+'-'+id+'.mp4'
        # print(name)
        # print(title)
        # os.system('pwd')
        # os.system("mv "+name.replace(' ','\ ')+" "+(title+'.mp4').replace(' ','\ '))
        # sys.exit()
        # ydl_options = {
        #     #'outtmpl': '%(id)s.%(ext)s',  # use the video id for filename
        #     'outtmpl':title,
        #     'writethumbnail': False,
        #     'no_warnings': True,
        #     'continuedl': False,
        #     'restrictfilenames': True,
        #     'quiet': False,
        #     'writesubtitles': True,
        #     'format': "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]"}
        # with youtube_dl.YoutubeDL(ydl_options) as ydl:
        #     try:
        #         ydl.add_default_info_extractors()
        #         vinfo = ydl.extract_info(video_url, download=True)
        #     except (youtube_dl.utils.DownloadError, youtube_dl.utils.ContentTooShortError, youtube_dl.utils.ExtractorError) as e:
        #         print('error_occured')

# downloader('dUqjCnIkDeI','/home/kolibri','Sample')


def makeFolders(path):
    '''
    Used to generate the folder structure.
    '''
	if os.path.isdir(path):
		pass
	else:
		os.mkdir("%s" %path)
	os.chdir("%s" %path)

count=0

travel_df = pd.read_excel('/home/kolibri/Divya/Maharashtra2/MH 5-10 Videos.xlsx')
print(type(travel_df))
# print(travel_df)


'''
To filter the dataframe
'''
travel_df=travel_df.loc[travel_df['subject_name']=="Maths"]

travel_df=travel_df.loc[travel_df['Flag']=="Y"]
print(type(travel_df))

'''
To generate dictionay from dataframe.
'''
travel_dict = travel_df.to_dict('index')
print(travel_dict)

loc= "/home/kolibri/Divya/Maharashtra2/Content-MH"
os.chdir("%s" %loc)
# print(lst)
data_sorted_by_syllabusName = sorted(travel_dict.values(),key=lambda x:x['syllabus_name'])
data_grouped_by_syllabusName = groupby(data_sorted_by_syllabusName, key=itemgetter('syllabus_name'))
# print(lst)
# data_grouped_by_syllabusName = itertools.groupby(rows, key=lambda each: each['syllabus_name'])
# for syllabusName, data1 in data_grouped_by_syllabusName:


'''
Nested for-loops to parse the dictionary and generate the folder structure and call the downloader function  to download videos.
'''
for syllabusName, data1 in data_grouped_by_syllabusName:
	print(syllabusName)
	makeFolders(syllabusName)
	data_sorted_by_subjectName = sorted(data1, key=itemgetter('subject_name'))
	data_grouped_by_subjectName = groupby(data_sorted_by_subjectName, key=itemgetter('subject_name'))
	# data_grouped_by_subjectName=itertools.groupby(data1,key=lambda each: each['subject_name'] )
	for subjectName, data2 in data_grouped_by_subjectName:
		print(subjectName)
		makeFolders(subjectName)
		data_sorted_by_chapter_name = sorted(data2, key=itemgetter('chapter_name'))
		data_grouped_by_chapter_name = groupby(data_sorted_by_chapter_name, key=itemgetter('chapter_name'))

		# data_grouped_by_chapterName=itertools.groupby(data2,key=lambda each: each['chapter_name'] )
		for chapterName, data3 in data_grouped_by_chapter_name:
			print(chapterName)
			makeFolders(chapterName)
			data_sorted_by_tuName = sorted(data3, key=itemgetter('tu_name'))
			data_grouped_by_tuName = groupby(data_sorted_by_tuName, key=itemgetter('tu_name'))


			# data_grouped_by_tuName=itertools.groupby(data3,key=lambda each: each['tu_name'] )
			for tuName, data4 in data_grouped_by_tuName:
				print(tuName)
				makeFolders(tuName)
				# print(os.getcwd()+tuName)
								
				data_sorted_by_concat = sorted(data4, key=itemgetter('concat'))
				data_grouped_by_concat = groupby(data_sorted_by_concat, key=itemgetter('concat'))

				# data_grouped_by_concat=itertools.groupby(data4,key=lambda each: each['concat'] )
				lst=[]
				for concat, data5 in data_grouped_by_concat:
					print(concat)
					
					# fileName=os.getcwd()+"/"+concat
					# print(os.getcwd()+"/"+concat)
					c=0
					# print(data5)
					# for youtube_id, Full_Youtube_id in enumerate(data5):
					data_sorted_by_id = natsorted(data5, key=itemgetter('youtube_id'))
					data_grouped_by_id = groupby(data_sorted_by_id, key=itemgetter('youtube_id'))	
                    
                    '''
                    To copy the file to the required location if already downloaded.
                    If file already present at required location, then skip,
                    else download the video file.
                    '''
					for id1, data6 in data_grouped_by_id:
						title=str(concat)
						count+=1
						print(count)
						folderPath=os.getcwd()+"/"+title+".mp4"
						# fileName="/home/kolibri/Divya/Maharashtra/Topper-MH/MH-all"+"/"+title+".mp4"
						fileName2=folderPath.replace("Maharashtra2","Maharashtra",1)

						if c==0:
							lst.append(title)
							c+=1
							
						elif title in lst:
							title=title.replace(title,title+str(c),1)
							print(title)
							lst.append(title)
							c+=1
						else:
							pass							
						
						exists = os.path.isfile(fileName2)
						if not exists:
							downloader(str(id1),os.getcwd(),title)
						else:
							copyfile(fileName2, folderPath)
						pass


					# print(lst)
				p=loc+"/"+syllabusName+"/"+subjectName+"/"+chapterName
				os.chdir("%s" %p)

			p=loc+"/"+syllabusName+"/"+subjectName
			os.chdir("%s" %p)


		p=loc+"/"+syllabusName
		os.chdir("%s" %p)

	os.chdir("%s"%loc)

# break

print("-------------------------")
