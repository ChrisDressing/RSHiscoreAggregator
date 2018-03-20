from lxml import html
import requests
from bs4 import BeautifulSoup


f = open('/root/RSHiscoreAggregator/Players.txt', 'r')
out = open('/root/RSHiscoreAggregator/Initial.txt', 'w')
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
	#1 == Attack, 2 == Defence, 3 == Strength, 4 == Constitution, 5 == Ranged, 7 == Magic
        try:
            while x < 27:
                    if x == 18:# or x == 19:
                            rank, level, xp = statList[x].split(',');print(xp)

                            total += int(xp)
                    x+=1
        except:
               print("There was a problem with the current player")
        out.write(name + "," + str(total) + " ")
f.close()
out.close()
