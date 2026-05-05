
from file import INDEXER_PATH
import os
import json
from settings import data

class Finder :
    
    @staticmethod
    def findByKeyword(keywords:list[str]):
        found = [] # list of indexers found in file
        for file in os.listdir(INDEXER_PATH) :
            with open(f"{INDEXER_PATH}{file}",'r') as filedata :
                data = json.load(filedata)
                for keyword in keywords :
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
            if f in folder or folder in f:
                return True
        return False
        

    @staticmethod
    def getNewFiles():
        import os.path
        # get paths to search in
        file_to_search_in = data["paths_to_search_in"]
        from settings import loadSettings , ext_to_ignore , path_to_ignore
        loadSettings()
        from file import File
        # walk over

        new_files = []
        print(file_to_search_in)
        i = 0
        for search_path in file_to_search_in :
            print(f"searching in {search_path} =====>")
            for path, directories, files in os.walk(f"{search_path}"):
                for file in files :
                    full_path = os.path.join(path, file)
                    # check if not one of ignored extensions or files
                    ext = file.split(".")[-1]
                    if ext in ext_to_ignore or Finder.isIgnored(path) :
                        # print("ignoring " , file , " at " , path)
                        print(f"ignored {i} files")
                    else :
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
        print("LOADED " , len(indexed), " INDEXED")
        # search for file paths that are not in indexed
        return [i for i in newFiles if i not in indexed]
    
    @staticmethod
    def getScannerFiles():
        from file import File , SCANNED_PATH
        indexed = [File.loadScanned(filename)["path"] for filename in os.listdir(SCANNED_PATH)]

    @staticmethod
    def generateScannedId():
        from file import SCANNED_PATH
        i = 0
        while os.path.exists(f"{SCANNED_PATH}{i}"):
            i += 1
        return i

    @staticmethod
    def saveScannerFiles():
        from file import File
        for path in Finder.getNewFiles() :
            File.saveScanner(f"{Finder.generateScannedId()}",path)
        print("Sauvegardé")
    
Finder.saveScannerFiles()