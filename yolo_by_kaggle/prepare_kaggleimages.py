from argparse import ArgumentParser
import os
import sys

import shutil
import re
import zipfile

from pathlib import Path

global opts
opts = {}

def parseOptions():
    argparser = ArgumentParser()
    argparser.add_argument('--dwn', help=':downloaling data set', action='store_true') # use action='store_true' as flag
    argparser.add_argument('--zip', help=':specify kagglecatsanddogs_3367a.zip') # use action='store_true' as flag
    args = argparser.parse_args()
    if args.dwn: opts.update({'dwn':args.dwn})
    if args.zip: opts.update({'zip':args.zip})

if __name__ == '__main__':
    parseOptions()
    if ('dwn' in opts.keys()):
        os.system(r'curl -LO https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip')

    if ('zip' in opts.keys()):
        org_dir = './PetImages'
        dst_dir = './images'

        if os.path.isdir(org_dir):
            shutil.rmtree(org_dir)
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)

        with zipfile.ZipFile(opts['zip']) as existing_zip:
            existing_zip.extractall('./')
        os.remove('./MSR-LA - 3467.docx')
        os.remove('./readme[1].txt')
        os.makedirs(dst_dir)

        p = Path(org_dir)
        image_ary = list(p.glob("**/*.jpg"))
        for image in image_ary:
            m = re.findall('PetImages\/(\w+)\/(\d+)\.jpg', str(image))
            if m[0]:
                cat = m[0][0]
                num = int(m[0][1])
                dst_file = '%s/%s%08d.jpg' % (dst_dir, cat, num)
                print('mv %s to %s' % (image, dst_file))
                shutil.move(image, dst_file)

        if os.path.isdir(org_dir):
            shutil.rmtree(org_dir)
