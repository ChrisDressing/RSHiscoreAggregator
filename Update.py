import locale
import time
import datetime
from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
import concurrent.futures

def process(line):
        playerName, xp, levels = line.split(",")
        if xp == "D":
            print(playerName + " has an issue with the hiscores")
        else:
            page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + playerName)
            data = page.text
            soup = BeautifulSoup(data, "lxml")
            stats = str(soup.p.extract())
            stats = stats.strip("<p>").strip("</p>")
            statList = stats.split()
            x = 0
            total = 0
            curlevel = 0
            for x in skillsList:
                rank, level, curXP = statList[x].split(',')
                total += int(curXP)
                curlevel += int(level)
            total = total - int(xp)
            totalL = curlevel - int(levels)
            print(playerName + " " + str(total) + " " + str(totalL))
            return playerName, total, totalL

skillsList = [0]
inFileName = "Initial.txt"
outFileName = "standings.html"
competitionName = "Double XP Weekend"
if sys.argv[1] != "":
    if sys.argv[1] == "dxp":
        skillsList = [0]
        inFileName = "DxpInitial.txt"
        outFileName = "dxpstandings.html"
        competitionName = "Double XP Weekend"
    if sys.argv[1] == "artisan":
        skillsList = [8,10,12,13,14,16,21,23]
        inFileName = "ArtisanInitial.txt"
        outFileName = "artisanstandings.html"
        competitionName = "Artisan Skills"
    if sys.argv[1] == "combatant":
        skillsList = [1,2,3,4,5,6,7,24]
        inFileName = "CombatantInitial.txt"
        outFileName = "combatantstandings.html"
        competitionName = "Combatant Skills"
    if sys.argv[1] == "gatherer":
        skillsList = [9,11,15,20,22,26]
        inFileName = "GathererInitial.txt"
        outFileName = "gathererstandings.html"
        competitionName = "Gatherer Skills"
    if sys.argv[1] == "support":
        skillsList = [17,18,19,25,27]
        inFileName = "SupportInitial.txt"
        outFileName = "supportstandings.html"
        competitionName = "Support Skills"

ts = time.time()
locale.setlocale(locale.LC_ALL, '')
readIn = open('/root/RSHiscoreAggregator/'+inFileName, 'r')
data = readIn.read().strip()
playerData = data.split(" ")
total = -1
totalxp = []
playerNames = []
totalLevels = []

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    future_process = {executor.submit(process, element): element for element in playerData}
    for future in concurrent.futures.as_completed(future_process):
        try:
            exceptionThing = future_process[future]
            tName, txp, tLevel = future.result()
            totalxp.append(txp)
            playerNames.append(tName)
            totalLevels.append(tLevel)
        except Exception as e:
            print("ERROR:" + str(e))
            continue

totalxp, playerNames, totalLevels = zip(*sorted(zip(totalxp, playerNames, totalLevels)))
temp = len(totalxp) - 1
rank = 1
html = """<!DOCTYPE html><head><script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-103248346-1', 'auto');
  ga('send', 'pageview');

</script></head><body><h1>Welcome to the Alright """ + competitionName +""" Competition!</h1><p>"""
html += "<br><i><b>Note: This tracker updates once every 30 minutes or so, if it's not, please let Chris D know</b></i><br>"

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
html += "Last updated (UTC): " + st + "</p><br><table align=\"center\"><tr><th>Rank</th><th colspan = '2'>Player</th><th>XP Gained</th><th>Levels Gained</th></tr>";
while temp >= 0:
    html += "<tr><td>" + str(rank) + "</td><td><img class=\"avatar\" src=http://services.runescape.com/m=avatar-rs/" + playerNames[temp] + "/chat.gif></td><td><a href=http://www.runeclan.com/user/" + playerNames[temp] + ">" + playerNames[temp].replace("_", " ") + "</a></td><td>" + str(
        format(totalxp[temp], "n")) + "</td><td>" + str(totalLevels[temp]) + "</td></tr>"
    temp -= 1
    rank += 1
html += "</table></body></html>"
readOut = open('/var/www/html/'+outFileName, 'w')
readOut.write(html)

print("Users processed:" + str(len(totalxp)))
