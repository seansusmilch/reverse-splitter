from .common import get_real_url
import requests
import requests_random_user_agent # type: ignore
from bs4 import BeautifulSoup


def find_press_release(query:str):
    session = requests.Session()
    
    res = session.get('https://search.yahoo.com/search', params={'p': query})
    soup = BeautifulSoup(res.text, 'html.parser')
    search_results = soup.select(':is(p, h3).title > a')
    for result in search_results:
        if 'news.search.yahoo.com' in result['href']:
            continue
        print(result['href'])
        real_url = get_real_url(result['href'])
        res = session.get(real_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return real_url, soup.get_text()
    
    return None


if __name__ == '__main__':
    print(find_press_release('SONN reverse split press release'))