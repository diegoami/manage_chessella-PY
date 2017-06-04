import glob
import os
import re

RAW_DIR='from_cbase_raw/'
WORK_DIR='work/'

import traceback
import ntpath


import argparse

def retrieve_all_files():
    pgns = glob.glob(RAW_DIR+'*.pgn')
    return pgns

def retrieve_file(fileIn):
    with open(RAW_DIR+fileIn, "r") as handle:
        lines = handle.readlines()
        pgnStr = '\n'.join([line.strip() for line in lines if len(line.strip()) > 0]).strip()
        return pgnStr



def remove_comments(pgnStr):
    pgnStr = re.sub('\{[\s\%0-9s:]+\}','',pgnStr)
    pgnStr = re.sub('\{\s*\([\s0-9s:]+\)\s*\}','',pgnStr)
    pgnStr = re.sub('\{\s*\[\%emt [\s0-9s:]+\]\s*\}', '', pgnStr)

    return pgnStr

def write_file(cnt, fileOut):
    with open(WORK_DIR+fileOut, "w") as handle:
        handle.write(cnt)

def sep_headers(cnt):
    return cnt.replace('"] ','"]\n').replace('"][','"]\n[')

def hanging_brackets(cnt):
    while True:
        m = re.search('(\[[a-zA-Z0-9]+\s*)\n(\s*\"[a-zA-Z0-9\,\s\:\/\-\.]+\"\])',cnt) or re.search('(\[[a-zA-Z0-9]+\s*\"[a-zA-Z0-9\,\s\:\/\-\.]+)\n(\s*[a-zA-Z0-9\,\s\:\/\-\.]+\"\])',cnt)
        if m:
            print(m.groups())
            cnt = cnt[:m.end(1)]+' '+cnt[m.start(2):]
        else:
            break

    return cnt


def add_new_lines(cnt):
    ncnt = cnt
    nc,ls = 0,0
    insq = False
    for i,c in enumerate(cnt):
        nc += 1
        if c == '[' and nc <=j  :
            insq = True
        if c == ']':
            insq = False
        if c == '\n':
            nc = 0
        if (c == ' '):
            ls = i
        if nc >=80 and not insq:
            ncnt= ncnt[:ls]+'\n'+ncnt[ls+1:]
            nc = i-ls

    return ncnt

if __name__ == "__main__":

    pgnFiles =retrieve_all_files()
    for pgnFileC in pgnFiles:
        pgnFile = ntpath.basename(pgnFileC)

        pgnStr = retrieve_file(pgnFile)
    
        pgnStr = sep_headers(pgnStr)
        pgnStr = hanging_brackets(pgnStr)
        pgnStr = remove_comments(pgnStr)
        pgnStr = add_new_lines(pgnStr)
    
        write_file(pgnStr, pgnFile)
        print(pgnFile)
