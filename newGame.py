import mariadb
import sys
from riotwatcher import LolWatcher, ApiError
import json

#"SELECT max(gameKDA), idLeagueMatch FROM leagueMatch WHERE dateType = "day""



def newGame(accountId, newGameDataJson):
    functionKda = newGameDataJson

    sql = "SELECT gameKDA from leagueMatch where leaguePlayerId = ? "
    val = (accountId)

    print()

