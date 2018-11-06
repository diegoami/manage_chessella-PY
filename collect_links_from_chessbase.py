
ROOT_PAGE='https://en.chessbase.com'
ROOT_POST_PAGE=ROOT_PAGE+'/post/'

import argparse
import os
import requests
from bs4 import BeautifulSoup
import re
import sys
def read_all_links(directory):
    all_links = []
    for filename in os.listdir(directory):
        if filename.endswith(".lst"):
            total_path = os.path.join(directory, filename)
            print("Processing {}".format(total_path))
            with open(total_path , 'r') as file_handle:
                all_lines = file_handle.readlines()
                all_links += [line.replace('http://', 'https://').rstrip() for line in all_lines]
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
    parser.add_argument('--out')

    args = parser.parse_args()
    if (args.out) and os.path.isfile('chessbase_links/'+args.out):
        print('{} file exists...Exiting'.format(args.out))
        exit(0)
    read_links = read_all_links('chessbase_links')
    page_num = 0
    found = False
    to_parse_links = []
    while not found:
        link_to_parse = 'https://en.chessbase.com/{}'.format(page_num)
        print('Examining {}'.format(link_to_parse))
        all_posts = retrieve_posts_page(link_to_parse)
        for post in all_posts:
            if post in read_links:
                found = True
                print('Found {} in history'.format(post))
            else:
                to_parse_links.append(post)
                print(post)
        page_num += 1
    if args.out:
        fout = open('chessbase_links/'+args.out,'a')
    else:
        fout = sys.stdout
    for link in to_parse_links:
        print(link, file=fout)
    fout.close()
