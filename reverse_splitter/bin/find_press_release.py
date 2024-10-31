import requests
import requests_random_user_agent # type: ignore
from bs4 import BeautifulSoup
import reverse_splitter.bin.logger as logger
from urllib3.util import parse_url
from urllib.parse import unquote

log = logger.setup_logger('PressRelease')

site_blacklist = [
    'businesswire.com',
    'reddit.com',
    'www.nasdaqtrader.com',
    'seekingalpha.com',
    'x.com',
    'sec.gov',
    'stackexchange.com'
]

def is_blacklisted(url: str):
    for site in site_blacklist:
        if site in url:
            return True
    return False

def get_real_url(raw_url):
    parsed_url = parse_url(raw_url)
    paths = parsed_url.path.split('/')
    for element in paths:
        if element.startswith('RU='):
            return unquote(element).replace('RU=', '')

def find_press_release(query:str):
    session = requests.Session()
    
    res = session.get('https://search.yahoo.com/search', params={'p': query})
    soup = BeautifulSoup(res.text, 'html.parser')
    search_results = soup.select(':is(p, h3).title > a')
    print(len(search_results))
    for result in search_results:
        if 'news.search.yahoo.com' in result['href']:
            continue
        log.debug(f'Found press release: {result.text}')
        real_url = get_real_url(result['href'])
        
        if is_blacklisted(real_url):
            log.debug(f'Blacklisted site: {real_url}')
            continue
        
        try:
            res = session.get(real_url, timeout=5)
        except Exception as e:
            log.error(f'Error fetching {real_url} - {e}')
            continue
        
        soup = BeautifulSoup(res.text, 'html.parser')
        text_content = soup.get_text()
        
        if len(text_content) < 1000:
            log.debug(f'Press release looks short. Assuming something went wrong {real_url} content="{text_content}"')
            continue
        
        return real_url, text_content
    
    return None


if __name__ == '__main__':
    import reverse_splitter.bin.gemini_summarizer as gemini
    url, article = find_press_release('"NA" reverse stock split "fractional"')
    print(url)
    print(len(article))
    
    print(gemini.summarize_article(article))