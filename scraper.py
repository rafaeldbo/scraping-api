import requests
from bs4 import BeautifulSoup, Tag

from database import Noticia

def extract_noticia(noticia_tag:Tag) -> Noticia | None:
    try:
        return Noticia(
            titulo = noticia_tag.select('a.feed-post-link')[0].findChildren('p')[0].text.strip(),
            link = noticia_tag.select('a.feed-post-link')[0].get('href'),
            tema = noticia_tag.select('span.feed-post-metadata-section')[0].text.strip(),
            tempo_publicacao = noticia_tag.select('span.feed-post-datetime')[0].text.strip()
        )
    except Exception as e:
        return None

def scraping_g1() -> list[dict[str, str]]:
    page = requests.get('https://g1.globo.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    feed_noticias = soup.select('div.feed-root')[0].select('div.feed-post-body')

    return [extract_noticia(noticia) for noticia in feed_noticias]


if __name__ == '__main__':
    print('\n\n'.join(f'{i}: {noticia}' for i, noticia in enumerate(scraping_g1())))