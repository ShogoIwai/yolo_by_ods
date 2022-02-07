from argparse import ArgumentParser
import re
import shutil

global opts
opts = {}

def parseOptions():
    argparser = ArgumentParser()
    argparser.add_argument('--file', help=':specify replace file') # use action='store_true' as flag
    argparser.add_argument('--pre',  help=':specify pre regular expression') # use action='store_true' as flag
    argparser.add_argument('--post', help=':specify post regular expression') # use action='store_true' as flag
    args = argparser.parse_args()
    if args.file: opts.update({'file':args.file})
    if args.pre: opts.update({'pre':args.pre})
    if args.post: opts.update({'post':args.post})

def replace():
    infile = opts['file']
    outfile = opts['file'] + '.tmp'
    ofs = open(outfile, mode='w')
    with open(infile) as file:
        for line in file:
            line.rstrip()
            line = re.sub(opts['pre'], opts['post'], line)
            ofs.write(line)
    ofs.close()
    shutil.move(outfile, infile)

if __name__ == '__main__':
    parseOptions()
    if ('file' in opts.keys() and 'pre' in opts.keys() and 'post' in opts.keys()):
        replace()
