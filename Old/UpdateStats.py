import os
import sys
from database import databaseConnect
import pickle
from PlayerData import Player
import time
import os
import sys

kaas = os.path.join(sys.path[0],"PlayerData")
lijst = []
for file in os.listdir(os.path.join(kaas)):
    lijst.append(file)

mydb = databaseConnect()

def getDataFromPlayer(accountId):
    file = "PlayerData/" + accountId
    data = open(os.path.join(sys.path[0],file), 'rb')
    return_data = pickle.load(data)
    data.close()
    return return_data

def update_players():
    mycursor = mydb.cursor()  # connect naar de DB om alle spelers te krijgen die meedoen
    sql_select_Query = "select * from Players"
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()
    x = 0
    for row in records:
        print(x)
        if x >=20:
            time.sleep(123)
            x = 0



        if row[2] not in lijst:
            Player(row[1], row[2],"euw1")
            print("new player " + row[1])

        x = x +  update(row[2])

def update(player):
    x = 1
    player = getDataFromPlayer(player)
    old = player.lastGameId
    print(old)
    #player.updateSummoner()
    player.getMatchHistory() # +1
    #player.updateRank()
    new = player.lastGameId
    player.saveObject()
    print(new)
    if old != new:
        player.getMatchData() # api = 1
        x = x+1
        player.saveObject()
        print("New game: " + player.name)

    return x
if __name__ == '__main__':
    #main()
    update_players()
    mydb.close()
    


    
