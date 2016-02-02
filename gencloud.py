#!/usr/bin/env python2
"""
Using custom colors
====================
Using the recolor method and custom coloring functions.
"""

import feedparser
import os
import json
import sys
import string

from os import path
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, get_single_color_func
from bs4 import BeautifulSoup


def scrapenwrite(feeds, output_dir):
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    with open(path.join(output_dir, 'allposts.txt'), "w") as g:
        for feed in feeds:
            d = feedparser.parse(feed)
            with open(path.join(output_dir, d.feed.title + '.txt').encode('utf8'), "w") as f:
                for item in d.entries:
                    soup = BeautifulSoup(item.summary)
                    contents = "\n".join(soup.stripped_strings)
                    f.write(contents.encode('utf8'))
                    g.write(contents.encode('utf8'))


def generate_word_cloud(text, mask_filename, output_image, stop_words,
                        max_words=1000):
    d = path.dirname(__file__)  # get basename to prepend to mask_filename
    mask = imread(path.join(d, mask_filename))

    # adding specific stopwords
    stopwords = STOPWORDS.copy()
    for word in stop_words:
        stopwords.add(word)
    for letter in string.letters:
        stopwords.add(letter)

    wc = WordCloud(max_words=max_words, mask=mask, stopwords=stopwords,
                   margin=10, random_state=1).generate(text)

    wc.recolor(color_func=get_single_color_func('grey'), random_state=3)

    wc.to_file(output_image)

with open(sys.argv[1]) as config_file:
    conf = json.load(config_file)

scrapenwrite(feeds=conf['feeds'], output_dir=conf['output_dir'])
if conf.get('each_corpi'):
    files = os.listdir(conf['output_dir'])
else:
    files = ['allposts.txt']
for filename in files:
    if filename[-4:] != '.txt':
        continue
    if filename == 'allposts.txt':
        output_image = conf['output_image']
    else:
        output_image = filename + ".png"
    with open(path.join(conf['output_dir'], filename)) as corpus:
        text = corpus.read()
        generate_word_cloud(
            text=text,
            mask_filename=conf['mask_filename'],
            output_image=path.join(conf['output_dir'], output_image),
            stop_words=conf['stop_words'],
            max_words=conf['max_words'],
        )
