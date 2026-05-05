import os
import json




INDEXER_PATH = "src/indexes/"

class File :
    
    def __init__(self,path:str,tags:list[str], description:str):
        self.path = path
        self.tags = tags
        self.description = description
        # check if file is deleted from the its source 
        self.deleted = os.path.exists(self.path)
    def saveFileDescription(self):
        # save the file infos to the search indexer

        pass
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


if __name__ == "__main__":
    print([os.path.exists(i) for i in File.PathsToSearchIn()])
    # File.upload(
    #     "/rr",
    #     ["one","two","three"],
    #     description="pour le travail"
    # )
    # File.upload(
    #     "/rr",
    #     ["one","two","three"],
    #     description="pour le sport"
    # )
    # File.upload(
    #     "/rr",
    #     ["one","two","three"],
    #     description="pour le travail"
    # )
