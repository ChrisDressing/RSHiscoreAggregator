import locale
import time
import datetime
from lxml import html
import requests
from bs4 import BeautifulSoup

ts = time.time()
locale.setlocale(locale.LC_ALL, '')
readIn = open('/root/RSHiscoreAggregator/Initial.txt', 'r')
# readOut = open('/var/www/html/index.html', 'w')
data = readIn.read().strip()
playerData = data.split(" ")
total = -1
totalxp = []
playerNames = []

for line in playerData:
    try:
        playerName, xp = line.split(",")
        if xp == "D":
            print(playerName + " has an issue with the hiscores")
        else:
            playerNames.append(playerName)
            page = requests.get('http://services.runescape.com/m=hiscore/index_lite.ws?player=' + playerName)
            data = page.text
            soup = BeautifulSoup(data, "lxml")
            stats = str(soup.p.extract())
            stats = stats.strip("<p>").strip("</p>")
            statList = stats.split()
            x = 0
            total = 0
            # 1 == Attack, 2 == Defence, 3 == Strength, 4 == Constitution, 5 == Ranged, 7 == Magic
            while x < 30:
                if x == 15:  # or x == 19:
                    rank, level, curXP = statList[x].split(',')
                    total += int(curXP)
                    # break;
                x += 1
            total = total - int(xp)
            totalxp.append(total)
            print(playerName + " " + str(total))
            # readOut.write(playerName + "," + str(total) + "<br>")
    except:
        print("There was an error with the user: " + playerName)
        totalxp.append(-1);

totalxp, playerNames = zip(*sorted(zip(totalxp, playerNames)))
temp = len(totalxp) - 1
rank = 1
html = """<!DOCTYPE html><head><script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-103248346-1', 'auto');
  ga('send', 'pageview');

</script><link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\"><meta http-equiv=\"Cache-control\" content=\"no-cache\"></head><body><h1>Welcome to the Casual Oasis Mining Competition!</h1><p>"""
html += "<br><i><b>Note: This tracker updates once every 30 minutes or so, if it's not, please let Chris D know</b></i><br>"

# ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
html += "Last updated (UTC): " + st + "</p><br><table align=\"center\"><tr><th>Rank</th><th colspan = '2'>Player</th><th>XP Gained</th></tr>";
while temp >= 0:
    html += "<tr><td>" + str(rank) + "</td><td><img src=http://services.runescape.com/m=avatar-rs/" + playerNames[temp] + "/chat.gif></td><td><a href=http://www.runeclan.com/user/" + playerNames[temp] + ">" + playerNames[temp].replace("_", " ") + "</a></td><td>" + str(
        format(totalxp[temp], "n")) + "</td></tr>"
    temp -= 1
    rank += 1
html += "</table></body></html>"
# html+="</p><br><i><b>Note: This tracker updates once every 15 minutes or so, if it's not, please let Chris D know</b></i></body></html>"
readOut = open('/var/www/html/index.html', 'w')
readOut.write(html)
