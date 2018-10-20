
ROOT_PAGE='https://en.chessbase.com'
ROOT_POST_PAGE=ROOT_PAGE+'/post/'

import argparse
import os
import requests
from bs4 import BeautifulSoup
import re

def read_all_links(directory):
    all_links = []
    for filename in os.listdir(directory):
        if filename.endswith(".lst"):
            total_path = os.path.join(directory, filename)
            print("Processing {}".format(total_path))
            with open(total_path , 'r') as file_handle:
                all_lines = file_handle.readlines()
                all_links += all_lines
    return all_links

def retrieve_posts_page(pageLink):
    r = requests.get(pageLink)
    soup = BeautifulSoup(r.content)
    if not soup:
        return None

    all_posts = soup.find_all('a', attrs={'href': re.compile("post")})
    all_links = set([convert_tag(post['href']) for post in all_posts])
    return all_links

def convert_tag(tag_link):
    if (tag_link.startswith('/post')):
        tag_link = ROOT_PAGE + tag_link
    if '#' in tag_link:
        tag_link = tag_link.split('#')[0]
    return tag_link

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug')
    args = parser.parse_args()
    read_links = read_all_links('chessbase_links')
    all_posts = retrieve_posts_page('https://en.chessbase.com/0')
    print(all_posts)