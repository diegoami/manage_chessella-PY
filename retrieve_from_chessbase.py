import requests
from bs4 import BeautifulSoup
import re
import os
ROOT_PAGE='http://en.chessbase.com'
ROOT_POST_PAGE=ROOT_PAGE+'/post/'
import traceback

import argparse

def iscbreplay_dataurl(tag):
    return tag.has_attr('data-url')

def iscbreplay_text(tag):
    if tag.has_attr('class')  :
        return tag.has_attr('class') and not tag.has_attr('data-url') and 'cbreplay' in tag.attrs['class']

def get_pgnlinks_from_page(pageLink,debug=True):
    pgnstrings =[]
    print(pageLink)
    r = requests.get(pageLink)
    soup = BeautifulSoup(r.content)
    if not soup:
        return None

    cbreplays_text = soup.find_all(iscbreplay_text)

    cbreplays_dataurl = soup.find_all(iscbreplay_dataurl)
    for cbreplay in cbreplays_dataurl :
        pgnstrings.append( {"data-url":cbreplay.attrs['data-url']})

    for cbreplay in cbreplays_text:
        pgnstrings.append({"pgn-text": cbreplay.get_text()})

    return pgnstrings

def downoad_files(data_urls ):
    for data_url in data_urls:
        r =requests.get(ROOT_PAGE+data_url)
        if not os.path.exists("from_cbase"):
            os.makedirs("from_cbase")
        dfile = "from_cbase/"+ data_url.lower().replace('/','_').replace('\\','_').replace('_portals_all_','')
        with open(dfile , "w",encoding='utf-8') as handle:
            norlines = r.text.replace('\r\n','\n')
            handle.write(norlines)

def downoad_pgns(pgn_texts, page_link):
    for index, pgn_text in enumerate(pgn_texts):
        if not os.path.exists("from_cbase_raw"):
            os.makedirs("from_cbase_raw")
        dfile = "from_cbase_raw/"+  page_link.replace(ROOT_POST_PAGE,'')+'_'+str(index)+'.pgn'
        with open(dfile , "w",encoding='utf-8') as handle:
            handle.write(pgn_text)


def process_page(page_link):

    page_link = page_link if ROOT_POST_PAGE in page_link else ROOT_POST_PAGE + page_link
    pgnlinks = get_pgnlinks_from_page(page_link, debug=True)
    print(pgnlinks)
    data_urls = [x["data-url"] for x in pgnlinks if "data-url" in x]
    downoad_files(data_urls)
    pgn_texts = [x["pgn-text"] for x in pgnlinks if "pgn-text" in x]
    downoad_pgns(pgn_texts, page_link)


def retrieve_games(fileLink):
    with open(fileLink, "r") as handle:
        lines = handle.readlines()
        for line in lines:
            if (line.startswith('#')):
                continue
            print("Processing %s" % line)
            try:
                process_page(line.strip())
            except:
                print("Could not process page %s " % line.strip())

                traceback.print_exc()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--fileLink')
    parser.add_argument('--debug')
    args = parser.parse_args()

    retrieve_games(args.fileLink)