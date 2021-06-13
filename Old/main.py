
from new import main
from UpdateStats import update_players
import time

def mainLoop():
    update_players()
    time.sleep(10)
    main()


if __name__ == '__main__':
    mainLoop()
    