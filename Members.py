import fileinput
import requests

#The URL to get the guild members is http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=casual+escape
fw = open('/root/RSHiscoreAggregator/members_lite.ws','w',encoding = "ISO-8859-1")
page = requests.get('http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=casual+oasis');
fw.write(page.text)
fw.close()
f = open('/root/RSHiscoreAggregator/members_lite.ws', encoding = "ISO-8859-1")
out = open('/root/RSHiscoreAggregator/Players.txt', 'w')
#playerList = f.read().replace(" ", "_").split()
temp = 0
g = ""
with fileinput.input('/root/RSHiscoreAggregator/members_lite.ws', openhook=fileinput.hook_encoded("iso-8859-1")) as fileT:
    for line in fileT:
        if temp != 0:
            tempLine = line.replace(" ", "_")
            name = line.split(",")
            tempName = name[0].replace(" ","_").replace("\xa0","_")
            print(tempName)
            g+=tempName+"\n"
        else:
            temp=1
        #print(fileinput.filename())
#g+="MadClikr\n"
out.write(g)
out.close()
