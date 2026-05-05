import json
import os

# paths_to_search_in = (
#     os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') , 
#     f"{os.environ['USERPROFILE']}/Documents", # documents
#     f"{os.environ['USERPROFILE']}/Downloads", # downloads
# )


# path_to_ignore = ()
# ext_to_ignore = (".env",".py",".html")

from file import File
paths_to_search_in = File.PathsToSearchIn()
path_to_ignore = ["projet_assistant_chat_de_IBRAHIM"]
ext_to_ignore = [".pyc",".py",".html",".css"]
scan_new_files = False


def saveParams():
    # save to json
    with open("src/params.json","w") as file :
        obj = {
            "paths_to_search_in" : paths_to_search_in,
            "path_to_ignore" : path_to_ignore,
            "ext_to_ignore" : ext_to_ignore,
            "scan_new_files":scan_new_files
        }
        json.dump(obj,file)
        
saveParams()
def loadSettings():
    with open("src/params.json","r") as file :
        d = json.load(file)
    return d


# update in vm
data = loadSettings()
paths_to_search_in = data["paths_to_search_in"]
path_to_ignore =  data["path_to_ignore"]
ext_to_ignore = data["ext_to_ignore"]
scan_new_files = data["scan_new_files"]


# if a path is ignored
def isIgnored(path:str):
    return path in data["path_to_ignore"] 