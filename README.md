# RSHiscoreAggregator
This project is meant for tracking experience points and levels gained for clan competitions in the video game, Runescape 3. 

# How to use
This project is comprised of 3 python scripts that do different functions

- `members.py`  collects a list of users in a clan, by default this collects from the clan, Alright.

- `hiscore.py` using the list of players from `members.py`, it grabs the initial xp of each clan member for the given competition
- `update.py` using the result of `hiscore.py`, it gathers what the current xp of each member is and subtracts it from the initial gatherings

# Scalability
Due to a recent concurrency update, this now scales much better than it used to. 
When run on the lowest tier DigitalOcean droplet, it can process 450 users in about 2 minutes and 30 seconds, prior to the concurrency update it used to take 20+ minutes. 
These scripts are not bound by CPU or IO, but rather how quickly Runescape's APIs process the requests.
