#!/usr/bin/env python3

import argparse
import urllib
import urllib.request
import sys
from lxml import html
from argparse import RawTextHelpFormatter


def show_langs():
    """This function shows available language pairs."""
    for k, v in ABBR:
        print(k, '--> {0}'.format(v))


def pretty_printer(contens, showall):
    """This function pretty prints the response received from multitran.com."""
    if not contens:
        print('Translation not found.')
    i = 0
    cats = -1
    if not showall:
        cats = 4
    for elem in contens:
        if elem.endswith('.'):
            i += 1
            if cats == i:
                break
            print(''.join(['\033[1m\x1B[3m', elem, '\x1B[23m\033[0m']))
        else:
            print(''.join([' "', elem, '"']))


def main(args):
    if args.langs:
        show_langs()
        sys.exit(0)
    if args.pair not in LANG:
        print('Please provide a valid language pair.')
        sys.exit(0)
    if not args.word:
        print('Please provide a valid word.')
        sys.exit(0)
    else:
        # sub whitespaces with '+' if a prhase
        args.word = '+'.join(args.word.split())

    multitran = "http://www.multitran.com/m.exe?l1={0}&l2={1}&s={2}"
    url = multitran.format(LANG[args.pair][0], LANG[args.pair][1], args.word)
    # splitting url into components
    parsed = urllib.parse.urlsplit(url)
    # encoding query word in utf-8
    encoded_query = urllib.parse.quote(parsed.query.encode('utf-8'))
    # joining splitted url back with encoded query
    url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path,
                                   encoded_query, parsed.fragment))
    with urllib.request.urlopen(url) as resp:
        fdata = resp.read()
        html_tree = html.fromstring(fdata)
    filtered = ''.join(['//table/tr/td[contains(@class, "subj")',
                        ' or contains(@class, "trans")]/a[@href]/text()'])
    text = html_tree.xpath(filtered)
    pretty_printer(text, args.all)


# lang constants
LANG = {'enru': [1, 2],
        'ruen': [2, 1],
        'ende': [1, 3],
        'deen': [3, 1],
        'deru': [2, 3],
        'rude': [3, 2],
        'enfr': [1, 4],
        'fren': [4, 1],
        'ensp': [1, 5],
        'spen': [5, 1],
        'enar': [1, 10],
        'aren': [10, 1],
        'enpl': [1, 14],
        'plen': [14, 1],
        'enzh': [1, 17],
        'zhen': [17, 1],
        'enit': [1, 23],
        'iten': [23, 1],
        'enja': [1, 28],
        'jaen': [28, 1],
        'ensw': [1, 29],
        'swen': [29, 1],
        'enuk': [1, 33],
        'uken': [33, 1]
        }

ABBR = (
        ('English - Russian', 'enru'),
        ('Russian - English', 'ruen'),
        ('German - Russian', 'deru'),
        ('Russian - German', 'rude'),
        ('English - German', 'ende'),
        ('German - English', 'deen'),
        ('English - French', 'enfr'),
        ('French - English', 'fren'),
        ('English - Spanish', 'ensp'),
        ('Spanish - English', 'spen'),
        ('English - Arabic', 'enar'),
        ('Arabic - English', 'aren'),
        ('English - Polish', 'enpl'),
        ('Polish - English', 'plen'),
        ('English - Chinese(Simp.)', 'enzh'),
        ('Chinese(Simp.) - English', 'zhen'),
        ('English - Italian', 'enit'),
        ('Italian - English', 'iten'),
        ('English - Japanese', 'enja'),
        ('Japanese - English', 'jaen'),
        ('English - Swedish', 'ensw'),
        ('Swedish - English', 'swen')
        )


if __name__ == '__main__':
    prs = argparse.ArgumentParser(description="""
    This is a simple client for multitran.com -- a multi-language online
    dictionary. \n
    USAGE:
        multirun deen Baum,
        multirun enru "penny dreadful",
        multirun -a enru tree
        """, formatter_class=RawTextHelpFormatter)
    prs.add_argument('pair', nargs='?', type=str,
                     help='Specify a language pair (enru, ruen, ende etc.)')
    prs.add_argument('word', nargs='?', type=str,
                     help='Specify a word to translate.')
    prs.add_argument('-a', '--all',
                     action='store_true',
                     help='Show all translations in all categories.',
                     required=False)
    prs.add_argument('-l', '--langs', action='store_true',
                     help='Show available language pairs.',
                     required=False)
    # prs.add_argument('-gui', '--gui',
    #                 action='store_true',
    #                 help='Run GUI client instead of console.',
    #                 required=False)
    prs.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = prs.parse_args()
    main(args)
