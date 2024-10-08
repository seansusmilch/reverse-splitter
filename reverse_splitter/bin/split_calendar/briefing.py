# https://hosting.briefing.com/cschwab/Calendars/SplitsCalendar.htm

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from typing import List
from reverse_splitter.bin.types import Split
import reverse_splitter.bin.logger as logger

log = logger.setup_logger('Briefing')

def scrape_briefing() -> List[Split]:
    
    def convert_date(raw_date):
        return datetime.strptime(raw_date, '%b %d').replace(year=datetime.today().year).strftime('%Y-%m-%d')
    
    url = 'https://hosting.briefing.com/cschwab/Calendars/SplitsCalendar.htm'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    rows = soup.select('tr')
    splits = []
    for row in rows:
        if not row.select_one('.rD,.rDa,.rL,.rLa'):
            continue
        
        cells = row.select('td')
        stock = cells[1].text
        exchange = 'NASDAQ/NYSE'
        company_name = cells[0].text
        ratio = cells[2].text.replace('-', ':')

        effective_date = convert_date(cells[4].text)
        # announced_date = convert_date(cells[5].text)
        splits.append(Split(stock, exchange, company_name, ratio, effective_date))
        
    return splits