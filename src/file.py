import os
import json




INDEXER_PATH = "src/indexes/"
SCANNED_PATH = "src/scan"

class File :
    
    def __init__(self,path:str,tags:list[str], description:str):
        self.path = path
        self.tags = tags
        self.description = description
        # check if file is deleted from the its source 
        self.deleted = os.path.exists(self.path)
    @staticmethod
    def getDesktopPath():
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

    @staticmethod
    def PathsToSearchIn():
        return (
            File.getDesktopPath() , 
            f"{os.environ['USERPROFILE']}/Documents", # documents
            f"{os.environ['USERPROFILE']}/Downloads", # downloads
        )
    
    @staticmethod
    def upload(path:str,keywords:list[str], description:str):
        """
        save the file infos to /indexer
        """
        
        # extract a unique id
        index = len(os.listdir(INDEXER_PATH) ) # make an id
        while os.path.exists(f"{INDEXER_PATH}/{index}.json"):
            index +=1 # until find unique index
        
        # extract file infos
        filename = path.replace("\\","/").split("/")[-1]

        with open(f"{INDEXER_PATH}{index}.json","w") as file:
            obj = {
                "filename":filename,
                "filepath":path,
                "description":description,
                "keywords" : keywords,
            }
            json.dump(obj,file)
    
    @staticmethod
    def loadIndexer(filename:str):
        """
            load indexer json data by its name
        """
        with open(f"{INDEXER_PATH}{filename}","r") as file :
            return json.load(file)
    @staticmethod
    def loadScanned(filename:str):
        """
            load indexer json data by its name
        """
        with open(f"{SCANNED_PATH}{filename}","r") as file :
            return json.load(file)
        
    @staticmethod
    def saveScanner(filename:str , path):
        with open(f"{SCANNED_PATH}{filename}","w") as file :
            obj = {
                "path":path
            }
            json.dump(obj,file)
