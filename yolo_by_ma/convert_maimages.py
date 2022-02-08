from argparse import ArgumentParser
import os
import sys

import shutil
import re
import requests
from bs4 import BeautifulSoup
import glob

sys.path.append(os.path.abspath('../common'))
from cdd import convert_darknettxt_dataset
from difPy import dif
from df  import df

global opts
opts = {}
imgsubdir = 'images'

def parseOptions():
    argparser = ArgumentParser()
    argparser.add_argument('--dwn',  help=':generate download script', action='store_true') # use action='store_true' as flag
    argparser.add_argument('--snm',  help=':specify number of start page') # use action='store_true' as flag
    argparser.add_argument('--psz',  help=':specify number of page size') # use action='store_true' as flag
    argparser.add_argument('--lim',  help=':specify number of image on each name') # use action='store_true' as flag
    argparser.add_argument('--conv', help=':convert image files', action='store_true') # use action='store_true' as flag
    args = argparser.parse_args()
    if args.dwn: opts.update({'dwn':args.dwn})
    if args.snm:  opts.update({'snm':args.snm})
    else: opts.update({'snm':1})   
    if args.psz:  opts.update({'psz':args.psz})
    else: opts.update({'psz':10})   
    if args.lim:  opts.update({'lim':args.lim})
    else: opts.update({'lim':10})   
    if args.conv: opts.update({'conv':args.conv})

if __name__ == '__main__':
    parseOptions()
    start_num = int(opts['snm'])
    page_size = int(opts['psz'])
    lim = int(opts['lim'])

    if ('dwn' in opts.keys()):
        if os.path.isfile('site.txt'):
            names = []

            urlSiteAry = convert_darknettxt_dataset.csvread('site.txt')
            for site_idx in range(2):
                urlSite = urlSiteAry[site_idx][0]
                try:
                    for i in range(page_size):
                        idx = str(start_num + i)
                        urlName = f"{urlSite}/{idx}/"
                        print(f"loading : {urlName} ...")
                        url = requests.get(urlName)
                        soup = BeautifulSoup(url.content, 'html.parser')

                        # for latest
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
                        # top-rated
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
        else:
            names = ['cat', 'dog']

        exe = 'python ~/rep/yolo_by_ods/common/gid/gid.py'
        KeywordAry = convert_darknettxt_dataset.csvread('kwd.txt')
        names = list(dict.fromkeys(names))

        dst_dir = f'./{imgsubdir}'
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        downcsh = f'{dst_dir}/down.sh'
        ofs = open(downcsh, mode='w')
        ofs.write(f"#!/usr/bin/env bash\n")
        for name in names:
            tgt = f"%s {name}" % (KeywordAry[0][0])
            knd = f"%s %s %s" % (KeywordAry[1][0], KeywordAry[1][1], KeywordAry[1][2])
            ofs.write(f"{exe} --tgt '{tgt}' --knd '{knd}' --lim {lim}\n")
        ofs.close()

    if ('conv' in opts.keys()):
        img_files = list(glob.glob(f'{imgsubdir}/*/*/*.jpg'))
        img_files.sort()
        # print(img_files)
        samples = []
        dupchk = {}
        for src in img_files:
            m = re.findall(f'{imgsubdir}\/(.*)\/(.*)\/.*.jpg$', src)
            if m[0]:
                idx = 0
                dst = f'{imgsubdir}/%s_%s_%08d.jpg' % (m[0][0], m[0][1], idx)
                while os.path.isfile(dst) or dst in dupchk.keys():
                    idx = idx + 1
                    dst = f'{imgsubdir}/%s_%s_%08d.jpg' % (m[0][0], m[0][1], idx)
                samples.append({"src": src, "dst": dst})
                dupchk[dst] = True
        for sample in samples:
            print('%s -> %s' % (sample['src'], sample['dst']))
            shutil.move(sample['src'], sample['dst'])

        convert_darknettxt_dataset.drop_empty_folders(imgsubdir)
        convert_darknettxt_dataset.drop_empty_folders(imgsubdir)

        dif(imgsubdir, delete=True)
        # df.img(imgsubdir)
        # df.prt()
        # df.mvp()
        # df.clr()
