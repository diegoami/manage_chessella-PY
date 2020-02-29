import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
import environment_data as env
from add_game_wf import do_add_game_workflow


SEARCH_PAGE = "http://newchessella.com/chessella/games/searchgamesform.action"



def get_games_number():
    r = requests.get(SEARCH_PAGE)
    soup = BeautifulSoup(r.content,"html.parser")

    if not soup or not soup.h3:
        return '0'
    search_in = soup.h3.string
    chess_games_matcher = re.search('Search in ([0-9]+.[0-9]{3}) \( mostly annotated \) chess games\!', search_in)
    if (chess_games_matcher):
        games_number = chess_games_matcher.group(1)
        return games_number
    else:
        return '0'


def verify_up():
    gamnum = get_games_number()
    return gamnum != None and gamnum != '0'



