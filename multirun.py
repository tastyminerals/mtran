#!/usr/bin/env python3

import argparse
from urllib import request
from lxml import html

def pretty_printer(contens):
    """This function pretty prints the response received from multitran.com."""
    for elem in contens:
        if elem.endswith('.'):
            print(''.join(['\033[1m\x1B[3m', elem, '\x1B[23m\033[0m']))
        else:
            print(''.join(['  "', elem, '"']))



def main(args):
    print(args)
    multitran = "http://www.multitran.com/m.exe?s={0}"
    with request.urlopen(multitran.format(args.word)) as resp:
        fdata = resp.read()
        html_tree = html.fromstring(fdata)
    text = html_tree.xpath(''.join(['//table/tr/td[contains(@class, "subj")',
                            ' or contains(@class, "trans")]/a[@href]/text()']))
    pretty_printer(text)



if __name__ == '__main__':
    prs = argparse.ArgumentParser(description="""
    This is a simple client for multitran.ru -- a multi-language online
    dictionary.""")
    prs.add_argument('langs', type=str,
                     help='Specify a language pair \
                     (enru, ruen, ende, deen, etc.)')
    prs.add_argument('word', type=str,
                     help='Specify a word to translate.')
    prs.add_argument('-gui', '--gui',
                     action='store_true',
                     help='Run GUI client instead of console.',
                     required=False)
    prs.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = prs.parse_args()
    main(args)
