import json
import os


def loadSetting() :
    projectFolder  = os.path.dirname (os.path.dirname(__file__))
    
    settingPath = os.path.join(projectFolder, "classicalRLSettings.json")
    
    with open(settingPath, "r", encoding = "utf-8") as file :
         return json.load(file)