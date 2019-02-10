from lxml import html
import requests
from bs4 import BeautifulSoup
import time
import sys

skillsList = [1]
outFileName = "Initial.txt"
if sys.argv[1] != "":
    if sys.argv[1] == "artisan":
        skillsList = [7,10,12,13,14,16,21,23]
        outFileName = "ArtisanInitial.txt"
    if sys.argv[1] == "combatant":
        skillsList = [1,2,3,4,5,6,7,24]
        outFileName = "CombatantInitial.txt"
    if sys.argv[1] == "gatherer":
        skillsList = [9,11,15,20,22,26]
        outFileName = "GathererInitial.txt"
    if sys.argv[1] == "support":
        skillsList = [17,18,19,25]
        outFileName = "SupportInitial.txt"

f = open('/root/RSHiscoreAggregator/Players.txt', 'r')
out = open('/root/RSHiscoreAggregator/'+outFileName, 'w')
playerList = f.read().split()

for name in playerList:
    print(name)
    page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + name)
    data = page.text
    soup = BeautifulSoup(data, "lxml")
    stats = str(soup.p.extract())
    stats = stats.strip("<p>").strip("</p>")
    statList = stats.split()
    x = 0
    total = 0
    totalLevels = 0
    # 1 == Attack, 2 == Defence, 3 == Strength, 4 == Constitution, 5 == Ranged, 7 == Magic
    disq = False
    attempts = 0
    try:
        for x in skillsList:
            rank, level, xp = statList[x].split(',')
            print(xp)
            while int(xp) <= 0 and attempts < 3:
                attempts += 1
                time.sleep(1)
                page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + name)
                data = page.text
                soup = BeautifulSoup(data, "lxml")
                stats = str(soup.p.extract())
                stats = stats.strip("<p>").strip("</p>")
                statList = stats.split()
                rank, level, xp = statList[x].split(',')
                print(xp)
            total += int(xp)
            totalLevels += int(level)
    except:
        print("There was a problem with the current player " + name + "... Trying again")
        disq = True
    if disq is True:
        out.write(name + "," + "D,D" + " ")
        disq = False
    else:
        out.write(name + "," + str(total) + "," + str(totalLevels) + " ")
f.close()
out.close()
'''
Overall 0      | Herblore 16
Attack  1      | Agility 17
Defence 2      | Thieving 18
Strength 3     | Slayer 19
Constitution 4 | Farming 20
Ranged 5       | Runecrafting 21
Prayer 6       | Hunter 22
Magic 7        | Construction 23
Cooking 8      | Summoning 24
Woodcutting 9  | Dungeoneering 25
Fletching 10   | Divination 26
Fishing 11     | Invention 27
Firemaking 12  |
Crafting 13    |
Smithing 14    |
Mining 15      | 
'''
