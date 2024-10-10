import requests
from bs4 import BeautifulSoup, Tag

from models import News

def extract_noticia(news_tag:Tag) -> News | None:
    try:
        return News(
            titulo = news_tag.select('a.feed-post-link')[0].findChildren('p')[0].text.strip(),
            link = news_tag.select('a.feed-post-link')[0].get('href'),
            tema = news_tag.select('span.feed-post-metadata-section')[0].text.strip(),
            tempo_publicacao = news_tag.select('span.feed-post-datetime')[0].text.strip()
        )
    except Exception as e:
        return None

def g1() -> list[dict[str, str]] | None:
    try:
        page = requests.get('https://g1.globo.com/')
    except TimeoutError as e:
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    feed_noticias = soup.select('div.feed-root')[0].select('div.feed-post-body')

    return [news for news in [extract_noticia(news) for news in feed_noticias] if news is not None]


if __name__ == '__main__':
    print('\n\n'.join(f'{i}: {news}' for i, news in enumerate(g1())))