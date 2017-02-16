
from lxml import html
import requests
from bs4 import BeautifulSoup

readIn = open('/home/pi/RSHiscoreAggregator/Initial.txt', 'r')
readOut = open('/var/www/html/index.html', 'w')
data = readIn.read().strip()
playerData = data.split(" ")
total = -1
totalxp = []
playerNames = []
for line in playerData:
        playerName, xp = line.split(",")
        playerNames.append(playerName)
        page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + playerName)
        data = page.text
        soup = BeautifulSoup(data, "lxml")
        stats = str(soup.p.extract())
        stats = stats.strip("<p>").strip("</p>")
        statList = stats.split()
        x = 1
        total = 0
	#1 == Attack, 2 == Defence, 3 == Strength, 4 == Constitution, 5 == Ranged, 7 == Magic
        while x < 8:
                if x != 6:
                        rank, level, curXP = statList[x].split(',')
                        total += int(curXP)
                x+=1
        total = total - int(xp)
        totalxp.append(total)
        print(playerName + " " + str(total))
	#readOut.write(playerName + "," + str(total) + "<br>")
totalxp, playerNames =  zip(*sorted(zip(totalxp, playerNames)))
temp = len(totalxp)-1
rank = 1
html = "<!DOCTYPE html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\"></head><body><h1>Welcome to the Casual Escape Test Competition!</h1><p>"
while temp >= 0:
        html+= str(rank) + ". " + playerNames[temp] + " - " + str(totalxp[temp]) + "<br>"
        temp-=1
        rank +=1
html+="</p><br><i><b>Note: This tracker updates once every 15 minutes or so, if it's not, please let Chris D know</b></i></body></html>"
readOut.write(html)
