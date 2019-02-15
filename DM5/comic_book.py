from bs4 import BeautifulSoup
import requests


def get_episodes(url):
    episodes = dict()

    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print('error status code: ' + str(response.status_code))
        return episodes

    soup = BeautifulSoup(response.text, 'lxml')

    chapterlistload = soup.find('div', id='chapterlistload')

    for chapter in chapterlistload.find_all('a', href=True, onclick=False):
        episodes[chapter['href'].split('/')[1]] = chapter.text

    return episodes
