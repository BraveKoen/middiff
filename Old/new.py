
from databaseUpdate import get_kda, get_current_stats, update_stats, update_week_inter
import datetime
from database import databaseConnect
import time
import PlayerData
import pickle
import sys
import os

champion_list = {'266': 'Aatrox', '103': 'Ahri', '84': 'Akali', '12': 'Alistar', '32': 'Amumu', '34': 'Anivia', '1': 'Annie', '523': 'Aphelios', '22': 'Ashe', '136': 'Aurelion Sol', '268': 'Azir', '432': 'Bard', '53': 'Blitzcrank', '63': 'Brand', '201': 'Braum', '51': 'Caitlyn', '164': 'Camille', '69': 'Cassiopeia', '31': "Cho'Gath", '42': 'Corki', '122': 'Darius', '131': 'Diana', '119': 'Draven', '36': 'DrMundo', '245': 'Ekko', '60': 'Elise', '28': 'Evelynn', '81': 'Ezreal', '9': 'Fiddlesticks', '114': 'Fiora', '105': 'Fizz', '3': 'Galio', '41': 'Gangplank', '86': 'Garen', '150': 'Gnar', '79': 'Gragas', '104': 'Graves', '120': 'Hecarim', '74': 'Heimerdinger', '420': 'Illaoi', '39': 'Irelia', '427': 'Ivern', '40': 'Janna', '59': 'Jarvan IV', '24': 'Jax', '126': 'Jayce', '202': 'Jhin', '222': 'Jinx', '145': "Kai'Sa", '429': 'Kalista', '43': 'Karma', '30': 'Karthus', '38': 'Kassadin', '55': 'Katarina', '10': 'Kayle', '141': 'Kayn', '85': 'Kennen', '121': "Kha'Zix", '203': 'Kindred', '240': 'Kled', '96': "Kog'Maw", '7': 'LeBlanc', '64': 'Lee Sin', '89': 'Leona', '876': 'Lillia', '127': 'Lissandra', '236': 'Lucian', '117': 'Lulu', '99': 'Lux', '54': 'Malphite', '90': 'Malzahar', '57': 'Maokai', '11': 'Master Yi', '21': 'Miss Fortune',
                 '62': 'Wukong', '82': 'Mordekaiser', '25': 'Morgana', '267': 'Nami', '75': 'Nasus', '111': 'Nautilus', '518': 'Neeko', '76': 'Nidalee', '56': 'Nocturne', '20': 'Nunu & Willump', '2': 'Olaf', '61': 'Orianna', '516': 'Ornn', '80': 'Pantheon', '78': 'Poppy', '555': 'Pyke', '246': 'Qiyana', '133': 'Quinn', '497': 'Rakan', '33': 'Rammus', '421': "Rek'Sai", '58': 'Renekton', '107': 'Rengar', '92': 'Riven', '68': 'Rumble', '13': 'Ryze', '113': 'Sejuani', '235': 'Senna', '875': 'Sett', '35': 'Shaco', '98': 'Shen', '102': 'Shyvana', '27': 'Singed', '14': 'Sion', '15': 'Sivir', '72': 'Skarner', '37': 'Sona', '16': 'Soraka', '50': 'Swain', '517': 'Sylas', '134': 'Syndra', '223': 'Tahm Kench', '163': 'Taliyah', '91': 'Talon', '44': 'Taric', '17': 'Teemo', '412': 'Thresh', '18': 'Tristana', '48': 'Trundle', '23': 'Tryndamere', '4': 'Twisted Fate', '29': 'Twitch', '77': 'Udyr', '6': 'Urgot', '110': 'Varus', '67': 'Vayne', '45': 'Veigar', '161': "Vel'Koz", '254': 'Vi', '112': 'Viktor', '8': 'Vladimir', '106': 'Volibear', '19': 'Warwick', '498': 'Xayah', '101': 'Xerath', '5': 'Xin Zhao', '157': 'Yasuo', '777': 'Yone', '83': 'Yorick', '350': 'Yuumi', '154': 'Zac', '238': 'Zed', '115': 'Ziggs', '26': 'Zilean', '142': 'Zoe', '143': 'Zyra'}


mydb = databaseConnect()

def getDataFromPlayer(accountId):
    file = "PlayerData/" + accountId
    data = open(os.path.join(sys.path[0],file), 'rb')
    return_data = pickle.load(data)
    data.close()
    return return_data

def main():
    print("execute")
    f = open(os.path.join(sys.path[0],"log.txt" ), "w")

    f.write("update time: " + datetime.datetime.now().strftime("%H:%M:%S"))



    stats_current = get_current_stats()  # krijg de kda van de inter en van de God

    KDA_int = stats_current[0]
    time_inter = stats_current[1]

    KDA_best = stats_current[2]
    time_best = stats_current[3]

    KDA_inter_week = stats_current[4]
    week_inter = stats_current[5]

    KDA_god_week = stats_current[6]
    week_god = stats_current[7]
    print(KDA_inter_week)
    print(week_god)

    week = datetime.date.today().isocalendar()[1]

    mycursor = mydb.cursor()  # connect naar de DB om alle spelers te krijgen die meedoen
    sql_select_Query = "select * from Players"
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()

    temp_int = []
    temp_name_int = ""

    temp_god = []
    temp_name_god = ""

    time_inter_week = 0
    time_god_week = 0

    for row in records:
        

        # [kills, deaths, assists, totalDamageDealt, win, champ, time_played, gameDuration]
        speler = getDataFromPlayer(row[2])
        stats = speler.getStats()
        rank = speler.rankedSolo
        lane = speler.getRole()
        spells = speler.getSpells()
        #geef het account id mee voor de stats
        day_inter = datetime.datetime.fromtimestamp(float(speler.lastTimePlayed/1000)).day

        KDA_new_inter = speler.get_kda()
        time_game = speler.matchData["gameDuration"]
        print("player {}, timeplayed = {}, kda= {}".format(row[1], day_inter, KDA_new_inter))
        

        if new_inter(KDA_int, time_inter, KDA_new_inter, day_inter, time_game):
            temp_int = [speler.name, day_inter, stats["kills"],
                        stats["deaths"], stats["assists"], stats["totalDamageDealtToChampions"] ,stats["win"], speler.matchHistory["matches"][0]["champion"], spells[0], spells[1], lane, rank[0],time_game]
            temp_name_int = speler.name
            KDA_int = KDA_new_inter
            time_inter = day_inter
            time_inter_week = time_game

        if new_god(KDA_best, time_best, KDA_new_inter, day_inter, time_game):
            temp_god = [speler.name, day_inter, stats["kills"],
                        stats["deaths"], stats["assists"], stats["totalDamageDealtToChampions"], stats["win"], speler.matchHistory["matches"][0]["champion"], spells[0], spells[1], lane, rank[0], time_game]
            temp_name_god = speler.name
            KDA_best = KDA_new_inter
            time_best = day_inter
            time_god_week = time_game
    
    if len(temp_int) != 0:
        print("Update trash")
        print(temp_name_int)
        update_stats(temp_name_int, "row[2]", temp_int[2], temp_int[3], temp_int[4], temp_int[5], temp_int[6], champion_list[str(temp_int[7])], temp_int[8], temp_int[9], temp_int[10], temp_int[11], temp_int[12], 1)
        
        if new_inter_week(KDA_inter_week, week_inter, KDA_int, week, time_inter_week):
            print("week")
            update_week_inter(temp_name_int, week, temp_int[2], temp_int[3], temp_int[4], temp_int[5], temp_int[6], champion_list[str(
                temp_int[7])], temp_int[8], temp_int[9], temp_int[10], temp_int[11], temp_int[12], 3)


    if len(temp_god) != 0:
        print("Update god")
        print(temp_god)
        update_stats(temp_name_god, "boeie", temp_god[2], temp_god[3],
                     temp_god[4], temp_god[5], temp_god[6], champion_list[str(temp_god[7])], temp_god[8], temp_god[9], temp_god[10], temp_god[11], temp_god[12], 2)
        
        if new_inter_god(KDA_god_week, week_god, KDA_best, week, time_god_week):
            print("week")
            update_week_inter(temp_name_god, week, temp_god[2], temp_god[3],
                              temp_god[4], temp_god[5], temp_god[6], champion_list[str(temp_god[7])], temp_god[8], temp_god[9], temp_god[10], temp_god[11], temp_god[12], 4)
    f.close()
    
#update_stats(row[1], row[2], stats[0], stats[1], stats[2],stats[3], stats[4], champion_list[str(stats[5])])


def new_inter(ci_KDA, ci_day, ni_KDA, ni_day, ni_lenght_game):
    today = datetime.datetime.now()

    if ci_day < ni_day:
        return True
    if ni_KDA < ci_KDA and ni_lenght_game > 1140 and ni_day == today.day:
        return True
    return False


def new_god(cg_KDA, cg_day, ng_KDA, ng_day, ng_lenght_game):
    today = datetime.datetime.now()

    if cg_day < ng_day:
        return True
    if ng_KDA > cg_KDA and ng_lenght_game > 1140 and ng_day == today.day:
        return True
    return False


def topTien(kda):
    mycursor = mydb.cursor()  # connect naar de DB om alle spelers te krijgen die meedoen

    sql_select_Query = "select * from TopListTotal"
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()
    player_kda = kda
    for i in records:
        top = get_kda(i[2], i[3], i[4])
        if player_kda < top:
            return i[0]
    return -1


def new_inter_week(ci_KDA, ci_week, ni_KDA, ni_week, ni_lenght_game):
    print(ci_KDA)
    print(ci_week)
    print(ni_KDA)
    print(ni_week)
    print(ni_lenght_game)
    print("---")

    if ci_week < ni_week:
        return True
    if ni_KDA < ci_KDA and ni_lenght_game > 1140 and ni_week == ci_week:
        return True
    return False

def new_inter_god(ci_KDA, ci_week, ni_KDA, ni_week, ni_lenght_game):
    print(ci_KDA)
    print(ci_week)
    print(ni_KDA)
    print(ni_week)
    print(ni_lenght_game)
    print("---")

    if ci_week < ni_week:
        return True
    if ni_KDA > ci_KDA and ni_lenght_game > 1140 and ni_week == ci_week:
        return True
    return False


if __name__ == "__main__":
    main()
    
