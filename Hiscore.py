import html
import requests
from bs4 import BeautifulSoup
import time
import sys
import concurrent.futures


def process(name):
    print(name)
    page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + name)
    data = page.text
    soup = BeautifulSoup(data, "lxml")
    if(soup.p is not None):
        stats = str(soup.p.extract())
        stats = stats.strip("<p>").strip("</p>")
        statList = stats.split()
        x = 0
        total = 0
        totalLevels = 0
        # 1 == Attack, 2 == Defence, 3 == Strength, 4 == Constitution, 5 == Ranged, 7 == Magic
        disq = False
        attempts = 0
        for x in skillsList:
            while True:
                try:
                    rank, level, xp = statList[x].split(',')
                    print(xp)
                    while int(xp) <= 0 and attempts < 3:
                        time.sleep(1); attempts+=1
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
                    break
                except:
                    print("There was a problem with the current player " + name + "... Trying again")
                    if attempts < 3:
                        attempts += 1
                        time.sleep(5)
                        continue
                    else:
                        disq = True
                        break
        if disq is True:
            print("Possible inactive player: " + name)
            return name + "," + "D,D" + " "
        else:
            return name + "," + str(total) + "," + str(totalLevels) + " "


skillsList = [0]
outFileName = "Initial.txt"
if sys.argv[1] != "":
    if sys.argv[1] == "dxp":
        skillsList = [0]
        outFileName = "DxpInitial.txt"
        competitionName = "Double XP Weekend"
    if sys.argv[1] == "artisan":
        skillsList = [8,10,12,13,14,16,21,23]
        outFileName = "ArtisanInitial.txt"
    if sys.argv[1] == "combatant":
        skillsList = [1,2,3,4,5,6,7,24]
        outFileName = "CombatantInitial.txt"
    if sys.argv[1] == "gatherer":
        skillsList = [9,11,15,20,22,26]
        outFileName = "GathererInitial.txt"
    if sys.argv[1] == "support":
        skillsList = [17,18,19,25,27]
        outFileName = "SupportInitial.txt"

f = open('/root/RSHiscoreAggregator/Players.txt', 'r')
out = open('/root/RSHiscoreAggregator/'+outFileName, 'w')
playerList = f.read().split()

finalStr = ''
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    future_process = {executor.submit(process, element): element for element in playerList}
    for future in concurrent.futures.as_completed(future_process):
        try:
            exceptionThing = future_process[future]
            finalStr += future.result()
        except Exception as e:
            print("Inactive player: " + exceptionThing)
            continue
out.write(finalStr)
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
