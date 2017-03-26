import fileinput
#The URL to get the guild members is http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=casual+escape

f = open('members_lite.ws', 'r')
out = open('Players.txt', 'w')
playerList = f.read().replace(" ", "_").split()
temp = 0
g = ""
with fileinput.input('members_lite.ws') as f:
    for line in f:
        if temp != 0:
        	tempLine = line.replace(" ", "_")
        	name = line.split(",")
        	tempName = name[0].replace("\xa0","_")
        	print(tempName)
        	g+=tempName+"\n"
        else:
        	temp=1

out.write(g)