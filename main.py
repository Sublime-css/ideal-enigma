import os
from os import path, system
import requests
import json
from fuzzywuzzy import fuzz

#limit for similarity of fuzzy string matching
#100 = only show perfect matches, 0 = show everything
fuzzy_search_limit = 50

#should only historical skins show?
historical_skins = False

#location of skin JSON file
json_url = 'https://sublime-css.github.io/ideal-enigma/'
parse=json.loads(requests.get(json_url).content)

#common game install locations
directories = [ "C:/Program Files (x86)/Steam/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "C:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "D:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                "E:/SteamLibrary/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/", 
                #non steam variant... i think?
                "C:/Program Files/1C Game Studios/IL-2/"]

def find_install():
    count = 0
    for directory in directories:
        if path.isdir(directory):
            print("Il-2 directory located at " + directory)
            count += 1

    if count == 0:
        print(  "Couldn't find your IL-2 installation automatically. Try placing the path, for example " +
                "C:/Program Files (x86)/Steam/steamapps/common/IL-2 Sturmovik Battle of Stalingrad/, into \"directory.txt\"")
        try:
            f = open("directory.txt", "r")
            f.readline()
            assert path.isdir(f.readline())
        except:
            print("IL-2 installation could not be located in the path specified in directory.txt(it should be on the second line)")
            system("Pause")
            exit(1)

    if count > 1:
        print("Yikes! You appear to have multiple IL-2 installations.")
        system("Pause")
        exit(2)
    return directory

#Downloading a skin:
def download(IL2_path, url, skin_path, name):
    print("Downloading...")
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

def print_results(search, airframe):
    print("""ID   Name                                         Airframe                 Creator
####################################################################################################""")
    for i in range(1, 1+ len(parse)):
        if(search == "none" or 
        fuzz.partial_ratio(search.lower(),parse[str(i)]["name"].lower()) > fuzzy_search_limit or 
        fuzz.partial_ratio(search.lower(),parse[str(i)]["airframe"].lower()) > fuzzy_search_limit or 
        fuzz.partial_ratio(search.lower(),parse[str(i)]["creator"].lower()) > fuzzy_search_limit ):
            if(historical_skins == False or parse[str(i)]["historical"] == "True"):
                if(airframe == "none" or fuzz.partial_token_sort_ratio(airframe, parse[str(i)]["airframe"]) > fuzzy_search_limit):
                    thestring = str(i) + " " * (5 - len(str(i)))
                    thestring += parse[str(i)]["name"] + " " * (45 - len(parse[str(i)]["name"])) 
                    thestring += parse[str(i)]["airframe"] + " " * (25 - len(parse[str(i)]["airframe"]))
                    thestring += parse[str(i)]["creator"] + " " * (25 - len(parse[str(i)]["creator"]))
                    thestring += "\n"
                    print(thestring)

find_install()

#idk why its named bob ok?
while True:
    bob = input("Commands: 'Search' (skin or creator), 'Filter' (by airframe), 'Historical'(toggle on and off). 'exit' to quit\nCommand: ")
    if (bob == "exit"):
        exit()
    elif (bob.lower() == "search"):
        print("Search Mode")
        while True:
            bob = input("Search term, for example 'FW190'. Press enter to exit search mode and return to normal operation.\nSearch: ")
            if (bob == ""):
                break
            print_results(bob, "none")
            while True:
                bob = input("Skin to sync, for example '1' to sync the skin with ID 1. Press enter to go back to search mode\n")
                if (bob == ""):
                    break
                try:
                    download("C:/Users/lukaa/Documents/IL-2/", parse[bob]["host"], parse[bob]["localpath"], parse[bob]["filename"])
                except:
                    print("Error! input out of bounds")
    elif (bob.lower() == "historical"):
        historical_skins = not historical_skins
        print("Historical only mode is", historical_skins)
    elif (bob.lower() == "filter"):
        print("Filter mode")
        while True:
            bob = input("Filter term, for example 'Spitfire'. Press enter to exit search mode and return to normal operation.\nSearch: ")
            if (bob == ""):
                break
            print_results("none", bob)
            while True:
                bob = input("Skin to sync, for example '1' to sync the skin with ID 1. Press enter to go back to search mode\n")
                if (bob == ""):
                    break
                try:
                    download("C:/Users/lukaa/Documents/IL-2/", parse[bob]["host"], parse[bob]["localpath"], parse[bob]["filename"])
                except:
                    print("Error! input out of bounds")