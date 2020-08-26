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
    for div in soup.find_all('div', class_="mat-txt"):
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
        author = soup.find_all('h1', class_="cln-nom")[0].contents[0]
    except:
        author = soup.find_all('span', class_="meta-item meta-aut")[0].contents[0].split(',')[0]
    return author

def get_title(soup):
    """Returns the title of the talk."""
    title = soup.find('h1', class_='mat-tit').contents[0]
    return title

# specify language
lang="pt-br"

links = [
    "https://olhardigital.com.br/colunistas/wagner_sanchez/post/o_futuro_cada_vez_mais_perto/78972",
    "https://olhardigital.com.br/colunistas/wagner_sanchez/post/os_riscos_do_machine_learning/80584",
    "https://olhardigital.com.br/ciencia-e-espaco/noticia/nova-teoria-diz-que-passado-presente-e-futuro-coexistem/97786",
    "https://olhardigital.com.br/noticia/inteligencia-artificial-da-ibm-consegue-prever-cancer-de-mama/87030",
    "https://olhardigital.com.br/ciencia-e-espaco/noticia/inteligencia-artificial-ajuda-a-nasa-a-projetar-novos-trajes-espaciais/102772",
    "https://olhardigital.com.br/colunistas/jorge_vargas_neto/post/como_a_inteligencia_artificial_pode_mudar_o_cenario_de_oferta_de_credito/78999",
    "https://olhardigital.com.br/ciencia-e-espaco/noticia/cientistas-criam-programa-poderoso-que-aprimora-deteccao-de-galaxias/100683"
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

    #with open(f'olhar_digital_{index}.json', 'w', encoding='utf-8') as f:
    #    json.dump(content, f, ensure_ascii=False, indent=4)



