from urllib.request import urlopen, HTTPError
import urllib.request
from config import key,channelId,file_path
import pathlib
import os
import json

# import distutils.dir_util
from pathlib import Path
# from config import key, channel_id, source_path, destination_path
from enum import Enum
import sys
import json
import os
from os.path import join
import re
from urllib.request import urlopen, HTTPError
from ricecooker.chefs import SushiChef
from ricecooker.classes import nodes, questions, files
from ricecooker.classes.licenses import get_license
from ricecooker.classes.files import VideoFile, HTMLZipFile, DocumentFile, YouTubeVideoFile
from ricecooker.exceptions import UnknownContentKindError, UnknownFileTypeError, UnknownQuestionTypeError, raise_for_invalid_channel
from le_utils.constants import content_kinds,file_formats, format_presets, licenses, exercises, languages
from pressurecooker.encodings import get_base64_encoding
import youtube_dl
import pprint
from multiprocessing import Pool
from pathlib import Path
import os 
# test video
final = []
#video_url='https://www.youtube.com/watch?v=bKbioetO4AE' # highres = 25MB
#video_url='https://vimeo.com/238190750' # lowres = 5MB
def downloader(id,p,title):
    # path = "/home/nalanda/Documents/video/"+id+".mp4"
    os.chdir(p)
    path = p+"/"+id+".mp4"
    # my_file = Path(path)
    print(path)
    if os.path.exists(path):
        print("Already Downloaded::", path)
    else:
        video_url = 'https://www.youtube.com/watch?v=' + id
        ydl_options = {
            #'outtmpl': '%(id)s.%(ext)s',  # use the video id for filename
            'outtmpl':title,
            'writethumbnail': False,
            'no_warnings': True,
            'continuedl': False,
            'restrictfilenames': True,
            'quiet': False,
            'writesubtitles': True,
            'format': "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]"}
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            try:
                ydl.add_default_info_extractors()
                vinfo = ydl.extract_info(video_url, download=True)
            except (youtube_dl.utils.DownloadError, youtube_dl.utils.ContentTooShortError, youtube_dl.utils.ExtractorError) as e:
                print('error_occured')


def callToDownloader(contents,title):
	for j in contents['items']:
		video_id=j['snippet']['resourceId']['videoId']
		final.append(video_id)
		# os.chdir(file_path)
		# p=file_path+"/"+title.replace(' ','_')
		# ti=j['snippet']['title']
		# video_id_list.append(ti)
		# print(title+"  "+ video_id)

		# downloader(video_id,p,ti)


channel_api="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId="+channelId+"&key="+key+"&maxResults=50"
conn = urlopen(channel_api)
SAMPLE_TREE = json.loads(conn.read().decode('utf-8'))
# print(SAMPLE_TREE)
print("#########")
print("channel:",SAMPLE_TREE['items'][0]['snippet']['channelTitle'])
file_path = file_path+(SAMPLE_TREE['items'][0]['snippet']['channelTitle']).replace(" ","_")
# print(file_path)

try:
	os.mkdir(file_path)
except OSError as exception:
	print(exception)


contents = urllib.request.urlopen(channel_api).read()
# print(contents)
# print(type(contents))
# print(SAMPLE_TREE)
video_id_list = []
for i in SAMPLE_TREE['items']:
	# print(i)
	# print(type(j))
	# print("Id:::",i['id'])
	# print("Title::",i['snippet']['title'])
	# print("########")
	title=i['snippet']['localized']['title']
	print("Title::",title)

	os.chdir(file_path)
	
	try:
		os.mkdir(title.replace(' ','_'))
	except OSError as exception:
		print("exception::",exception)

	



	playlist_id=i['id']
	# print(playlist_id)
	playlist_api="https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId="+playlist_id+"&key=AIzaSyAhDozjUdkiFN7Qh89BamscmGh0Y-DXE2E&maxResults=50"
	# print(playlist_api)

	conn = urlopen(playlist_api)
	contents = json.loads(conn.read().decode('utf-8'))
	
		

	count=1
	for j in contents['items']:
		if j['snippet']['position'] >=0:
			count=j['snippet']['position']

	# print(count)

	# print(contents)
	callToDownloader(contents,title)
	



	while "nextPageToken" in contents:
	# if i[nextPageToken] is not None:
		# print("*********")
		page_token=contents.get("nextPageToken")
		playlist_api="https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId="+playlist_id+"&key=AIzaSyAhDozjUdkiFN7Qh89BamscmGh0Y-DXE2E&maxResults=50&pageToken="+page_token
		# print(playlist_api)
		conn = urlopen(playlist_api)
		contents = json.loads(conn.read().decode('utf-8'))
		# print("*********")
		# count=50
		for j in contents['items']:
			if j['snippet']['position'] >=0:
				count=j['snippet']['position']
		callToDownloader(contents,title)


	count=count+1
		# print("Revised Count:",count)

	print(count)

	
		# print(p)
		# print(file_path+"/"+title)
		# print(video_id)
		# yt = pytube.YouTube("https://www.youtube.com/watch?v=jcZNsJXFQCA"+video_id)
		# print(yt)
		# video = yt.get('mp4', '720p')
		# video.download(file_path+"/"+title)



print("*********")
# print(video_id_list)

print(final)
print(len(final))
print(len(set(final)))