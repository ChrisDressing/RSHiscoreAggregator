from lxml import html
import requests
from bs4 import BeautifulSoup

readIn = open('Initial.txt', 'r')
readOut = open('/var/www/html/index.html', 'w')
data = readIn.read().strip()
playerData = data.split(" ")
total = -1
for line in playerData:
	playerName, xp = line.split(",")
	print(playerName + " " + xp)
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
	print(playerName + " " + str(total))
	readOut.write(playerName + "," + str(total) + "<br>")
