#!/usr/bin/env python3
import argparse
import requests
from lxml import html


def main(args):
    """Runner"""
    print(args)
    multitran = "http://www.multitran.com/m.exe?s={0}"
    with open('logg.xml', 'r') as f:
        fdata = f.read()
    #page = requests.get(multitran.format(args.word))
    #print(page.encoding)
    #page.encoding = 'cp1251'
    #print(page.text)
    html_tree = html.fromstring(fdata)
    #text = html_tree.xpath('/table/tr/td/text()')
    text = html_tree.xpath('//table/tr/td[@class="trans"]/a[@href]/text()')
    print(text)

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
