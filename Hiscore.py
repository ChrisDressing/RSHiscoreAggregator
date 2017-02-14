from lxml import html
import requests
from bs4 import BeautifulSoup


page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=XXXXXXXX')
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
		rank, level, xp = statList[x].split(',')
		total += int(xp)
	x+=1

print(total)
