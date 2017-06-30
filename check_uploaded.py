import requests
import re
from bs4 import BeautifulSoup
import pickle
import os

LAST_GAMES_PAGE = "http://www.amicabile.de/chessella/games/lastgames.action"
ROOT_PAGE       = "http://www.amicabile.de/chessella/games/"
PICKLE_FILE     = "filelist.dmp"

def get_games_list():
    r = requests.get(LAST_GAMES_PAGE)
    all_games_list = set()
    soup = BeautifulSoup(r.content,"html.parser")
    for a in soup.find_all('a', href=re.compile(r'showgame.action.*')):
        #if "showgame.action"  in a['href']:
        all_games_list.add(ROOT_PAGE+a['href'])
    return list(all_games_list)

def verify_valid_game(game):
    r = requests.get(game)
    soup = BeautifulSoup(r.content, "html.parser")
    boards_found = len(soup.find_all('a', href=re.compile(r'javascript:showBoard.*')))
    return boards_found




if __name__ == "__main__":

    if os.path.isfile(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as handle:
            games_map = pickle.load(handle)
    else:
        games_map= {}

    games_list = get_games_list()
    for game in games_list:
        m = re.search('\?id\=([0-9]+)',game)

        if not m:
            pass
        else:
            if m.group(1) in games_map:
                pass
            else:
                games_map[m.group(1)] = verify_valid_game(game)
            if games_map[m.group(1)] <=0 :
                print("Game {} does not have board".format(m.group(1)))

    with open(PICKLE_FILE, 'wb') as handle:
        pickle.dump(games_map, handle, protocol=pickle.HIGHEST_PROTOCOL)
