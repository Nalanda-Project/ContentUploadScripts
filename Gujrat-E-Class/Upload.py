
import json
import os
from os.path import join


from ricecooker.chefs import SushiChef
from ricecooker.classes import nodes, questions, files
from ricecooker.classes.licenses import get_license
from ricecooker.exceptions import UnknownContentKindError, UnknownFileTypeError, UnknownQuestionTypeError, raise_for_invalid_channel
from le_utils.constants import content_kinds,file_formats, format_presets, licenses, exercises, languages
from pressurecooker.encodings import get_base64_encoding

import random
import string
import re
from enum import Enum
# import uuid

# from Sample import SAMPLE_TREE as s
#from config import channelId


# SAMPLE_PERSEUS_1_JSON = open(join('/home/softcorner/Project/FolderStructurePrac','sample_perseus01.json'),'r').read()


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    files=[]
    
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
        
    else:
        d['type'] = "file"
        path = os.path.dirname(path)
        path = path+'/'+d['name']    
        #files.append(path)
        d['files']=[]
        #d['files']['path']=files
        dict={}
        dict['path']=path
        d['files'].append(dict)
    return d

#path='/home/softcorner/Project/FolderStructurePrac'

'''
def get_abspath(path, content_dir):
    """
    Replaces `content://` with absolute path of `content_dir`.
    By default looks for content in subdirectory `content` in current directory.
    """
    if path:
        file = re.search('Main/(.+)', path)
        if file:
            return os.path.join(content_dir, file.group(1))
    return path

'''

SAMPLE_TREE=[path_to_dict('/home/softcorner/Divya/Demo/content/Gujarat_e-Class')]


print(SAMPLE_TREE)

class Upload(SushiChef):
    """
    The chef class that takes care of uploading channel to the content curation server.
    We'll call its `main()` method from the command line script.
    """
    # channel_title=SAMPLE_TREE['items'][0]['snippet']['channelTitle']
    channel_info = {    #
        'CHANNEL_SOURCE_DOMAIN': 'gujrat_e_class@xyz',       # who is providing the content (e.g. learningequality.org)
        'CHANNEL_SOURCE_ID':"gujrat_e_class1" ,                   # channel's unique id
        'CHANNEL_TITLE': "Gujarat e-Class",
        'CHANNEL_LANGUAGE': 'en'

    }


    def construct_channel(self, *args, **kwargs):
        """
        Create ChannelNode and build topic tree.
        """
        channel = self.get_channel(*args, **kwargs)   # creates ChannelNode from data in self.channel_info
        print("sample tree::",SAMPLE_TREE)
        _build_tree(channel, SAMPLE_TREE)
        raise_for_invalid_channel(channel)
        return channel


# def generate_id(path):
#     """ Generate source_id based on text """
#     #return "".join(c for c in text.lower().replace(' ','-') if c.isalnum() or c == '-')[:200]
#     #print(path)
#     if path!=[]:
#         return str(uuid.uuid4())
#     else:
#         return ""

def _build_tree(node, sourcetree):
    #for child_source_node in sourcetree:
        #d=dict(child_source_node)
    #print(child_source_node)
        #title = child_source_node.replace(u'\xa0', u' ').replace('\n', '')
    #title="none"
    #title=""
    files=""
    for s in sourcetree:
        print(type(s))
        if s.get('type')=='file':
            title=str(s.get('name'))
            print("title:")
            print(title)
            files=s.get('files')


        else:
           # if child_source_node=='children':
            #for i in range(len(sourcetree.get('children'))):
             #   _build_tree(node,sourcetree.get('children')[i])
            #print(s)
            child_node = nodes.TopicNode(
                source_id=str(s.get('name')),
                title=str(s.get('name')).replace("_"," "),
            )
            node.add_child(child_node)

            source_tree_children = s.get("children", [])

            _build_tree(child_node, source_tree_children)
                
   
    #print("T:", title)
    #path="none"
     
    #source_id="none"
    
    #print("S:", source_id)

        #fancy_license = get_license(licenses.SPECIAL_PERMISSIONS, description='gfh', copyright_holder='sed')
    

    for child_source_node in sourcetree:    
        
            try:
                main_file = child_source_node['files'][0] if 'files' in child_source_node else {}
                kind = guess_content_kind(path=main_file.get('path'), web_video_data=main_file.get('youtube_id') or main_file.get('web_url'))
            except UnknownContentKindError:
                continue
            print("kind:")
            print(kind)
           
            # if kind == content_kinds.TOPIC:
            #     child_node = nodes.TopicNode(
            #         source_id=str(uuid.uuid4()),
            #         title=str(child_source_node.get('name'))
            #     )
            #     node.add_child(child_node)

                # source_tree_children = child_source_node.get("children", [])

                # _build_tree(child_node, source_tree_children)

            if kind == content_kinds.VIDEO:
                child_node = nodes.VideoNode(
                    # source_id=str(uuid.uuid4()),
                    source_id=str(child_source_node.get('name')).replace(' ','_'),
                    title=str(child_source_node.get('name').replace(".mp4","")),
                    license='All Rights Reserved',
                    copyright_holder= "Sarva Shiksha Abhiyaan",
                )
                add_files(child_node, child_source_node.get("files") or [])
                node.add_child(child_node)


            else:                   # unknown content file format
                continue

    return node

    
def guess_content_kind(path, web_video_data):
    """ guess_content_kind: determines what kind the content is
        Args:
            files (str or list): files associated with content
        Returns: string indicating node's kind
    """
    # If there are any questions, return exercise
   
    # See if any files match a content kind
    if path:
        # print("HEEEELLLLOOOO")
        ext = os.path.splitext(path)[1][1:].lower()
        if ext in content_kinds.MAPPING:
            return content_kinds.MAPPING[ext]
        raise InvalidFormatException("Invalid file type: Allowed formats are {0}".format([key for key, value in content_kinds.MAPPING.items()]))
    elif web_video_data:
        return content_kinds.VIDEO
    else:
        return content_kinds.TOPIC
    


def guess_file_type(kind, filepath=None):
    """ guess_file_class: determines what file the content is
        Args:
            filepath (str): filepath of file to check
        Returns: string indicating file's class
    """
     
    ext = os.path.splitext(filepath)[1][1:].lower()
    print("ext:"+ext)
    if kind in FILE_TYPE_MAPPING and ext in FILE_TYPE_MAPPING[kind]:
        return FILE_TYPE_MAPPING[kind][ext]
    return None


class FileTypes(Enum):
    """ Enum containing all file types Ricecooker can have
        Steps:
            AUDIO_FILE: mp3 files
            THUMBNAIL: png, jpg, or jpeg files
            DOCUMENT_FILE: pdf files
    """

    # DOCUMENT_FILE = 0
    # VIDEO_FILE = 1
    # THUMBNAIL = 2
    VIDEO_FILE = 0
    THUMBNAIL = 1


FILE_TYPE_MAPPING = {

  
    content_kinds.VIDEO : {
        file_formats.MP4 : FileTypes.VIDEO_FILE,
        #file_formats.VTT : FileTypes.SUBTITLE_FILE,
        file_formats.PNG : FileTypes.THUMBNAIL,
        file_formats.JPG : FileTypes.THUMBNAIL,
        file_formats.JPEG : FileTypes.THUMBNAIL,
    },
   
}

# LOCAL DIRS
EXAMPLES_DIR = os.path.dirname(os.path.realpath(__file__))
# DATA_DIR = os.path.join(EXAMPLES_DIR, 'data')
CONTENT_DIR = os.path.join(EXAMPLES_DIR, 'content')

def get_abspath(path, content_dir=CONTENT_DIR):
    """
    Replaces `content://` with absolute path of `content_dir`.
    By default looks for content in subdirectory `content` in current directory.
    """
    if path:
        file = re.search('content://(.+)', path)
        if file:
            return os.path.join(content_dir, file.group(1))
    return path



def add_files(node, file_list):
    for f in file_list:
        path=f.get('path')
        if path is not None:
            abspath = get_abspath(path)     # NEW: expand  content://  -->  ./content/  in file paths
        else:
            abspath = None

        print("kind:"+node.kind.upper())
         
        file_type = guess_file_type(node.kind, filepath=abspath)    

            
        if file_type == FileTypes.THUMBNAIL:
            node.add_file(files.ThumbnailFile(path=abspath))

        elif file_type == FileTypes.VIDEO_FILE:
            node.add_file(files.VideoFile(path=abspath, language=f.get('language')))
            
        else:
            raise UnknownFileTypeError("Unrecognized file type '{0}'".format(f['path']))   
    #node.add_file(files.VideoFile(path=abspath, language='en'))
 


if __name__ == '__main__':
    """
    This code will run when the sushi chef is called from the command line.
    """

    chef = Upload()
    chef.main()
