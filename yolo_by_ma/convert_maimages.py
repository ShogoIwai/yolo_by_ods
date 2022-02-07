from argparse import ArgumentParser
import os
import sys

import shutil
import re
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath('../common/cdd'))
import convert_darknettxt_dataset

global opts
opts = {}

def parseOptions():
    argparser = ArgumentParser()
    argparser.add_argument('--site', help=':specify site index') # use action='store_true' as flag
    argparser.add_argument('--snm',  help=':specify number of start page') # use action='store_true' as flag
    argparser.add_argument('--psz',  help=':specify number of page size') # use action='store_true' as flag
    argparser.add_argument('--lim',  help=':specify number of image on each name') # use action='store_true' as flag
    args = argparser.parse_args()
    if args.site: opts.update({'site':args.site})
    else: opts.update({'site':0}) 
    if args.snm:  opts.update({'snm':args.snm})
    else: opts.update({'snm':1})   
    if args.psz:  opts.update({'psz':args.psz})
    else: opts.update({'psz':10})   
    if args.lim:  opts.update({'lim':args.lim})
    else: opts.update({'lim':10})   

parseOptions()
site_idx = int(opts['site'])
urlSiteAry = convert_darknettxt_dataset.csvread('site.txt')
urlSite = urlSiteAry[site_idx][0]

start_num = int(opts['snm'])
page_size = int(opts['psz'])

names = []
names = ['hoge', 'fuga']
try:
    for i in range(page_size):
        idx = str(start_num + i)
        urlName = f"{urlSite}/{idx}/"
        print(f"loading : {urlName} ...")
        url = requests.get(urlName)
        soup = BeautifulSoup(url.content, 'html.parser')

        if (site_idx == 0):
            uls = soup.find_all('ul', class_='gallery-a e')
            if (not len(uls)): raise Exception
            for ul in uls:
                lis = ul.find_all('li')
                if (not len(lis)): raise Exception
                for li in lis:
                    tas = li.find_all('a')
                    if (not len(tas)): raise Exception
                    name = tas[1].text
                    # print(name)
                    names.append(name)
        if (site_idx == 1):
            uls = soup.find_all('ul', class_='gallery-a a d')
            if (not len(uls)): raise Exception
            for ul in uls:
                lis = ul.find_all('li')
                if (not len(lis)): raise Exception
                for li in lis:
                    spans = li.find_all('span')
                    if (not len(spans)): raise Exception
                    name = spans[0].text
                    # print(name)
                    names.append(name)
except Exception:
    pass

exe = 'python ~/rep/yolo_by_ods/common/gid/gid.py'
KeywordAry = convert_darknettxt_dataset.csvread('kwd.txt')
lim = int(opts['lim'])

downcsh = './down.sh'
ofs = open(downcsh, mode='w')
ofs.write(f"#!/usr/bin/env bash\n")
for name in names:
    tgt = f"%s {name}" % (KeywordAry[0][0])
    knd = f"%s %s %s" % (KeywordAry[1][0], KeywordAry[1][1], KeywordAry[1][2])
    ofs.write(f"{exe} --tgt '{tgt}' --knd '{knd}' --lim {lim}\n")
ofs.close()
