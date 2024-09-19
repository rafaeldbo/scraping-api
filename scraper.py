import requests
from bs4 import BeautifulSoup

from database import Noticia


def scraping_g1() -> list[dict[str, str]]:
    page = requests.get('https://g1.globo.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    feed_noticias = soup.select('div.feed-root')[0].select('div.feed-post-body')

    return [ Noticia(
        titulo = noticia.select('a.feed-post-link')[0].findChildren('p')[0].text.strip(),
        link = noticia.select('a.feed-post-link')[0].get('href').strip(),
        tema = noticia.select('span.feed-post-metadata-section')[0].text.strip(),
        tempo_publicacao = noticia.select('span.feed-post-datetime')[0].text.strip()
    ) for noticia in feed_noticias ]

