import pickle
from riotwatcher import LolWatcher, ApiError
import os
import sys
lol_watcher = LolWatcher("RGAPI-5e4fd7df-2085-4f7b-8b64-f696fd014c39")
class Player():
    matchHistory = []
    matchData = []
    summonerName = ""
    summonerId = ""
    accountId = ""
    currentAccountId = ""
    rankedSolo = ["unranked", "unranked"]
    rankedFlex = ["unranked", "unranked"]
    def __init__(self, name, accountId, region):
        self.name = name
        self.accountId = accountId
        self.region = region
        self.getMatchHistory(1)
        self.getMatchData()
        self.updateSummoner()
        self.saveObject()
    
    def getMatchHistory(self, aantal=10):
        match_history = lol_watcher.match.matchlist_by_account(self.region, self.accountId, None, None,None,None,aantal)#aantal games die je terug krijgt
        self.matchHistory = []
        self.matchHistory = match_history
        self.lastGameId = match_history['matches'][0]['gameId']
        self.lastTimePlayed = match_history['matches'][0]['timestamp']

    def getMatchData(self, matchNumber = 0): #welke match je wilt hebben
        if len(self.matchHistory) == 0 or len(self.matchHistory["matches"]) <= matchNumber:
            return False
        else:
            game_id = self.matchHistory['matches'][matchNumber]['gameId']
            match_data = lol_watcher.match.by_id(self.region, game_id)
            self.matchData = []
            self.matchData = match_data
            return True
    
    def updateSummoner(self):
        for i in self.matchData["participantIdentities"]:
            if i["player"]["accountId"] == self.accountId:
                self.summonerName = i["player"]["summonerName"]
                self.accountId = i["player"]["accountId"]
                self.summonerId = i["player"]["summonerId"]
                self.currentAccountId = i["player"]["currentAccountId"]
                return True
            
    
    def saveObject(self):
        file = "PlayerData/"+self.accountId
        with open(os.path.join(sys.path[0],file), 'wb') as gamefile:
            pickle.dump(self, gamefile ,pickle.HIGHEST_PROTOCOL)


    def getStats(self):
        for i in self.matchData["participantIdentities"]:
                if i["player"]["accountId"] == self.accountId:
                    participantId = i["participantId"]
                    break
        return self.matchData['participants'][participantId-1]["stats"]

    def getSpells(self):
        for i in self.matchData["participantIdentities"]:
            if i["player"]["accountId"] == self.accountId:
                participantId = i["participantId"]
                break
        spell1 = self.matchData['participants'][participantId-1]["spell1Id"]
        spell2 = self.matchData['participants'][participantId-1]["spell2Id"]
        return [spell1, spell2]
    
    def getRole(self):
        for i in self.matchData["participantIdentities"]:
            if i["player"]["accountId"] == self.accountId:
                participantId = i["participantId"]
                break
        role = self.matchData['participants'][participantId-1]["timeline"]["role"]
        lane = self.matchData['participants'][participantId-1]["timeline"]["lane"]
        
        if lane == "BOTTOM":
            if role == "DUO_CARRY":
                return "ADC"
            else: 
                return "SUPP"
        return lane

    def get_kda(self):
        stats = self.getStats()
        kills = stats["kills"]
        deaths = stats["deaths"]
        assists = stats["assists"]
        if deaths == 0:
            return kills + (assists * 0.66)
        return (kills + (assists * 0.66)) / deaths


    def updateRank(self):
        match_history = lol_watcher.league.by_summoner("euw1", self.summonerId)
        for i in match_history:
            print(i["queueType"])
            if i["queueType"] == "RANKED_FLEX_SR":
                print("update rank")
                self.rankedFlex = [i["tier"],i["rank"]]
            elif i["queueType"] == "RANKED_SOLO_5x5":
                self.rankedSolo = [i["tier"], i["rank"]]
