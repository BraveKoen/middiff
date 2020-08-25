from riotwatcher import LolWatcher, ApiError
import datetime
from database import databaseConnect

dt = datetime.datetime.today()
 
mydb = databaseConnect()


def update_stats(name, account_id, kills, deaths, assists, totalDamageDealt, win, champ,spellId1, spellId2, lane, rank, GameTime, row):
    mycursor = mydb.cursor()
    sql = "UPDATE Stats SET Name = %s, Time = %s, Kills = %s, Deaths = %s, Assists = %s, Damage = %s, Win = %s, ChampId = %s, spellId1 = %s, spellId2 = %s, lane = %s, rank = %s, GameTime = %s WHERE id = %s  "
    val = (name, dt.day, kills, deaths, assists, totalDamageDealt, win, champ,spellId1, spellId2, lane, rank, GameTime, row) # old 1

    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
    except:
        print("An exception occurred")


def update_week_inter(name, week, kills, deaths, assists, totalDamageDealt, win, champ, spellId1, spellId2, lane, rank, GameTime, row):
    mycursor = mydb.cursor()
    sql = "UPDATE Stats SET Name = %s, Time = %s, Kills = %s, Deaths = %s, Assists = %s, Damage = %s, Win = %s, ChampId = %s, spellId1 = %s, spellId2 = %s, lane = %s, rank = %s, GameTime = %s WHERE id = %s  "
    val = (name, week, kills, deaths, assists, totalDamageDealt, win,
           champ, spellId1, spellId2, lane, rank, GameTime, row)  # old 1

    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
    except:
        print("An exception occurred")

def get_kda(kills, deaths, assists):
    if deaths == 0:
        return kills + (assists * 0.66)
    return (kills + (assists * 0.66)) / deaths


def get_current_stats():
    mycursor = mydb.cursor()
    sql_select_Query = "select * from Stats"
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()
    KDA_inter = get_kda(records[0][4], records[0][5], records[0][6])
    KDA_god = get_kda(records[1][4], records[1][5], records[1][6])
    KDA_inter_week = get_kda(records[2][4], records[2][5], records[2][6])
    KDA_god_week = get_kda(records[3][4], records[3][5], records[3][6])

    return [KDA_inter, records[0][3], KDA_god, records[1][3], KDA_inter_week, records[2][3], KDA_god_week, records[3][3]]

