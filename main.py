from os import path, system
import requests
import json

url = 'https://sublime-css.github.io/ideal-enigma/'
request = requests.get(url)
parse=json.loads(request.content)
print(parse["name"])

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

if count > 1:
    print("Yikes! You appear to have multiple IL-2 installations.")