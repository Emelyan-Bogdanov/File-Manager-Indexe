
from file import INDEXER_PATH
import os
import json


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


