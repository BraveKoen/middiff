import mariadb
import sys
from riotwatcher import LolWatcher, ApiError
import json

lol_watcher = LolWatcher('RGAPI-045ebc7f-316a-477c-ab58-5c7a0bf483bd')

my_region = 'euw1'

try:
   conn = mariadb.connect(
      user="u94708p89384_DiscordBot",
      password="",
      host="185.104.29.102",
      database="u94708p89384_DiscordBot")
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)


cur = conn.cursor()
def addUser(first_name, last_name , leagName):
    statement = "INSERT INTO LeaguePlayerInfo (idLeaguePlayerInfo, PlayerAccountInfo, PlayerRankedInfo) VALUES (%s, %s, %s)"
    
    playerInfo = lol_watcher.summoner.by_name(my_region, leagName)
    playerRanked = lol_watcher.league.by_summoner(my_region, playerInfo['id'])

    try:
        val = (playerInfo['id'], json.dumps(playerInfo), json.dumps(playerRanked))
        cur.execute(statement, val)
    except:
        print("Error with adding user!")
        return
    statement = "INSERT INTO User (first_name, last_name, LeaguePlayerInfo) VALUES (%s, %s, %s)"
    val =(first_name, last_name, playerInfo['id'])
    cur.execute(statement, val)

sql = "SELECT gameKDA, gameDate from leagueMatch where leaguePlayerId= %s"
val = ("cGfTvcJtez69wBiG5uCX5jup6T1TOTxskcAsgZP_SC3YbIQ",)
cur.execute(sql, val)
print(cur.fetchall())



conn.close()