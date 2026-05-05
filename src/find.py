
from file import INDEXER_PATH
import os
import json
from settings import data

class Finder :
    
    @staticmethod
    def findByKeyword(keyword:list[str]):
        found = [] # list of indexers found in file
        for file in os.listdir(INDEXER_PATH) :
            with open(f"{INDEXER_PATH}{file}",'r') as filedata :
                data = json.load(filedata)
                if Finder.containsKeyword(keyword,data) :
                    found.append(file)
                
        return found # list of file indexers of this file

    @staticmethod
    def containsKeyword(keyword:str,filedata:dict):
        # if in tags or in description
        return keyword in filedata["description"] or keyword in filedata["keywords"]

    @staticmethod
    def isIgnored(folder:str):
        import settings
        # print(settings.data[""])
        for f in settings.data["path_to_ignore"] :
            if f in folder :
                return True
        return False
        

    @staticmethod
    def getNewFiles():
        import os.path
        # get paths to search in
        file_to_search_in = data["paths_to_search_in"]

        # walk over
        new_files = []
        for search_path in file_to_search_in :
            print(f"searching in {search_path} =====>")
            for path, directories, files in os.walk(f"{search_path}"):
                if Finder.isIgnored(path) :
                    # print("PATH",path)
                    # print("FILE",files)
                    # print("DIRECTORY",directories)
                    for file in files :
                        full_path = os.path.join(path, file)
                        new_files.append(full_path)
        return new_files
    
    @staticmethod
    def whatAreNewFiles(newFiles:list[str]):
        """
            compare scaned file and existant indexers , and returns only what is new
        """
        # load existant indexers
        from file import File
        
        # create a list of file paths that are indexed
        indexed = [File.loadIndexer(filename)["filepath"] for filename in os.listdir(INDEXER_PATH)]
        
        # search for file paths that are not in indexed
        return [i for i in newFiles if i not in indexed]
    
    @staticmethod
    def getScannerFiles():
        from file import File , SCANNED_PATH
        indexed = [File.loadScanned(filename)["path"] for filename in os.listdir(SCANNED_PATH)]

print(len(Finder.whatAreNewFiles(
    Finder.getNewFiles()
)))