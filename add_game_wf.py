import requests
import glob
import environment_data as env
from bs4 import BeautifulSoup
import os
from random import randint

HOST="http://www.amicabile.de"
 
LIST_PAGE = HOST+"/chessella/games/mygames.action"
LOGOUT_PAGE = HOST + "/chessella/user/logout.action"
LOGIN_PAGE = HOST + "/chessella/user/login.action"
SAVEPGN_PAGE = HOST + "/chessella/games/savepgn.action"
SUCCESS_STR = "These are your chess games"

def retrieve_random_pgn():
    pgns = glob.glob('./input/*.pgn')
    indxtoadd = randint(1,len(pgns))-1
    return pgns[indxtoadd]

def retrieve_game(pgn_filename):
    file = open(pgn_filename,'r',encoding='utf8')
    lines = file.read()
    file.close()
    return lines

def retrieve_filename_and_pgn():
    fp = retrieve_random_pgn()
    pgn_lines = retrieve_game(fp)
    return fp, pgn_lines

def do_login():
    s = requests.Session()
    s.post(LOGIN_PAGE , params=env.user_login_data)
    return s

def do_add_game(s,pgn_lines):
    out_params = {"publicgame":True, "pgnString": pgn_lines}
    r = s.post(SAVEPGN_PAGE, data=out_params)
    return r

def do_logout(s):
    s.get(LOGOUT_PAGE)

def do_add_game_workflow():
    filename, pgn_lines = retrieve_filename_and_pgn()
    print("Game "+filename+" scheduled to be added")
    s = do_login()
    r = do_add_game(s,pgn_lines)
    soup = BeautifulSoup(r.content,"html.parser")
    h2s = soup.find_all('h2')
    rettext = ""
    ok = True
    if len(h2s) > 0:
        os.rename(filename, filename+'.processed')
        rettext = filename + " successfully processed"
    else:
        rettext = " There seemed to be some problem with processing "+filename
        ok = False
    do_logout(s)
    return ok, rettext



