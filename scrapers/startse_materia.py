import re

from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json


def get_post(soup):
    """Returns post content as a single string.""" 
    post = ''
    post_strings = []
    for div in soup.find_all('section', class_="content-single"):
        for p in div.find_all('p'):
            # add every string in the post to a list
            post_strings.append(" ".join(p.text.split()))
        else:
            # after all strings have been added, create a single post string
            post = " ".join(post_strings)
    return post

def make_soup(url):
    """
    Return BeautifulSoup instance from URL
    :param str url:
    :rtype: bs4.BeautifulSoup
    """
    try:
        with urlopen(url) as res:
            # print("[DEBUG] in make_soup() : Found: {}".format(url))
            html = res.read()

    except HTTPError as e:
        print("[DEBUG] in make_soup() : Raise HTTPError exception:")
        print("[DEBUG] URL: {} {}".format(url, e))
        return None

    return BeautifulSoup(html, "lxml")

def get_author(soup):
    """Returns the author."""
    try:
        author = soup.find_all('h4', class_="title-single__info__author__about__name")[0].contents[1].contents[0]
    except:
        return ""
    return author

def get_title(soup):
    """Returns the title of the talk."""
    title = soup.find('h2', class_='title-single__title__name text-white fw-600').contents[0]
    return title

# specify language
lang="pt-br"

links = [
    "https://www.startse.com/noticia/startups/mobtech/deep-learning-o-cerebro-dos-carros-autonomos",
    ]   
    
for index,atl in enumerate(links):
    tr_soup = make_soup(atl)
    post = get_post(tr_soup)
    author = get_author(tr_soup)
    title = get_title(tr_soup)
    content = {
            'title': title,
            'author':author,
            "body":post,
            "type": "video",
            'url': atl
        }

    with open(f'startse_{index}.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)



