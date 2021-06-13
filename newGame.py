import mariadb
import sys
from riotwatcher import LolWatcher, ApiError
import json

#"SELECT max(gameKDA), idLeagueMatch FROM leagueMatch WHERE dateType = "day""