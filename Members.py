import fileinput
import requests

#The URL to get the guild members is http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=casual+escape
fw = open('/root/RSHiscoreAggregator/members_lite.ws','w',encoding = "ISO-8859-1")
page = requests.get('http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=alright');
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
g+="Anastasia\nBradleyjs\nCoolgang333\nChaoscrysay\nComp_Sci\nDr_Raat\nEvaluate\nGoJess\nGunnur\nhallmark\nIcer\nIR_CyClonE\nJay_Is_Jay\nJe_ss_e\nJoeyy\nJurassic\nJustin_D\nLucasai\nMade_in_Cali\nNanett\nNeokid90\nPingu_Btw\nRe_Akshon18\nRegicidal\nRonjac\nShaunyowns\nSnicket69\nSuity\nTryhard_MCB\nXeriana"
#g+="Emmett_Snake\n"
out.write(g)
out.close()
