import os
from os import path, system
import requests
import json

#location of skin JSON file
json_url = 'https://sublime-css.github.io/ideal-enigma/'

#common game install locations
directories = [ "C:/Program Files (x86)/Steam/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "C:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "D:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "E:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                #non steam variant... i think?
                "C:/Program Files/1C Game Studios/IL-2/"]

count = 0
for directory in directories:
    if path.isdir(directory):
        print("Il-2 directory located at " + directory)
        IL2_path = directory
        count += 1

if count == 0:
    print(  "Couldn't find your IL-2 installation automatically. Try placing the path, for example " +
            "C:/Program Files (x86)/Steam/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/, into \"directory.txt\"")
    system("Pause")
    exit(1)

if count > 1:
    print("Yikes! You appear to have multiple IL-2 installations.")
    system("Pause")
    exit(2)

#Downloading a skin:
def download(IL2_path, url, skin_path, name):
    try:
        skin=requests.get(url)
        if path.isdir(IL2_path) == True:
            if path.isdir(IL2_path + "data/graphics/skins/" + skin_path) != True:
                os.mkdir(IL2_path + "data/graphics/skins/" + skin_path)
            open(IL2_path + "data/graphics/skins/" + skin_path + name, 'wb').write(skin.content)
    except FileNotFoundError:
        print("Error writing to the IL-2 directory while syncing skin " + name + " to " + skin_path + ". No changes have been made.")
        return
        
    except Exception as e:
        print("Error while syncing skin " + name + " to " + skin_path)
        print(e)
        return
    print("Successfully synced skin " + name + " to " + skin_path)

print("""ID   Name                                         Airframe                 Creator
####################################################################################################""")

request = requests.get(json_url)
parse=json.loads(request.content)
for i in range(1, 1+ len(parse)):
    thestring = str(i) + " " * (5 - len(str(i)))
    thestring += parse[str(i)]["name"] + " " * (45 - len(parse[str(i)]["name"])) 
    thestring += parse[str(i)]["airframe"] + " " * (25 - len(parse[str(i)]["airframe"]))
    thestring += parse[str(i)]["creator"] + " " * (25 - len(parse[str(i)]["creator"]))
    print(thestring)

#download("C:/Users/lukaa/Documents/IL-2/", parse["1"]["host"], parse["1"]["localpath"], parse["1"]["filename"])
#download("C:/Users/lukaa/Documents/IL-2/", parse["2"]["host"], parse["2"]["localpath"], parse["2"]["filename"])
