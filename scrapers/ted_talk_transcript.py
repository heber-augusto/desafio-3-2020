import re

from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

def get_transcript_url(s, lang="en"):
    """
    Get a link from talk link to transcript
    :param str s:
    :rtype: str
    """
    r1 = "?language=" + lang
    r2 = "/transcript?language=" + lang

    is_match = re.match(".*(\?language=).*", s)
    if is_match:
        t_url = s.replace(r1, r2)
    else:
        t_url = s + r2

    return t_url


def get_transcript(soup):
    """Returns talk's transcript as a single string.""" 
    transcript = ''
    transcript_strings = []
    for div in soup.find_all('div', class_="Grid__cell flx-s:1 p-r:4"):
        for p in div.find_all('p'):
            # add every string in the transcript to a list
            transcript_strings.append(" ".join(p.text.split()))
        else:
            # after all strings have been added, create a single transcript string
            transcript = " ".join(transcript_strings)
    return transcript

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

def get_speaker_1(soup):
    """Returns the first speaker in TED's speaker list."""
    try:
        speaker_tag = re.findall(r"(?<=\"speakers\":).*?\"}]", str(soup))[0]
        # convert to DataFrame
        speakers_df = pd.read_json(speaker_tag)
        full_name_raw = (speakers_df.loc[:, 'firstname'] + ' '
                        + speakers_df.loc[:, 'middleinitial'] + ' '
                        + speakers_df.loc[:, 'lastname'])
        full_name_clean = full_name_raw.str.replace('\s+', ' ')
        # transform series to a dict
        speaker = full_name_clean.iloc[0]
    except:
        speaker = re.search(r"(?<=\"speaker_name\":)\"(.*?)\"", str(soup)).group(1)
    return speaker

def get_title(soup):
    """Returns the title of the talk."""
    title_tag = soup.find(attrs={'name': 'title'}).attrs['content']
    tag_list = title_tag.split(':')
    title = ":".join(tag_list[1:]).lstrip()
    return title

# specify language
lang="pt-br"

links = [
    "https://www.ted.com/talks/helen_czerski_the_fascinating_physics_of_everyday_life",
    "https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution",
    "https://www.ted.com/talks/sarah_parcak_help_discover_ancient_ruins_before_it_s_too_late",
    "https://www.ted.com/talks/sylvain_duranton_how_humans_and_ai_can_work_together_to_create_better_businesses",
    "https://www.ted.com/talks/chieko_asakawa_how_new_technology_helps_blind_people_explore_the_world",
    "https://www.ted.com/talks/pierre_barreau_how_ai_could_compose_a_personalized_soundtrack_to_your_life",
    "https://www.ted.com/talks/tom_gruber_how_ai_can_enhance_our_memory_work_and_social_lives"
    ]   
    
for index,atl in enumerate(links):
    tr_url = get_transcript_url(atl, lang)
    tr_soup = make_soup(tr_url)
    transcript = get_transcript(tr_soup)
    speaker = get_speaker_1(tr_soup)
    title = get_title(tr_soup)
    content = {
            'title': title,
            'author':speaker,
            "body":transcript,
            "type": "video",
            'url': tr_url
        }

    with open(f'ted_talk_{index}.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)



