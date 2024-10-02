# https://hedgefollow.com/upcoming-stock-splits.php
import os
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def scrape_hedgefollow():
    '''['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']'''
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=os.name != 'nt')
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://hedgefollow.com/upcoming-stock-splits.php', wait_until='domcontentloaded')

    # Get the table
    table = page.query_selector('table#latest_splits')
    rawTableData = table.evaluate('(tbl) => [...tbl.rows].map(r => [...r.cells].map(c => c.textContent))')

    browser.close()
    playwright.stop()
    
    tableData = list(filter(lambda row: len(row) == 6, rawTableData))

    return tableData

def scrape_briefing():
    
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
        exchange = 'NASDAQ'
        company_name = cells[0].text
        ratio = cells[2].text.replace('-', ':')

        effective_date = convert_date(cells[4].text)
        announced_date = convert_date(cells[5].text)
        splits.append([stock, exchange, company_name, ratio, effective_date, announced_date])
        
    return splits

def get_next_splits():
    '''
    Format: ['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']
    
    Need to:
    - Filter for reverse splits
    - Filter stock exchange (NASDAQ or NYSE)
    - Filter splits within the next x days
    '''
    all_splits = scrape_hedgefollow()
    for split in scrape_briefing():
        if list(filter(lambda r: r[0] == split[0], all_splits)): continue
        all_splits.append(split)
    
    reverse_splits = list(filter(lambda row: row[3].startswith('1:'), all_splits))
    
    stock_exchanges = ['NASDAQ', 'NYSE']
    reverse_splits = list(filter(lambda row: row[1] in stock_exchanges, reverse_splits))
    
    reverse_splits = list(filter(lambda row: datetime.today() <= datetime.strptime(row[4], '%Y-%m-%d'), reverse_splits))
    
    reverse_splits = sorted(reverse_splits, key=lambda row: datetime.strptime(row[4], '%Y-%m-%d'))
    
    return reverse_splits



if __name__ == '__main__':
    for split in get_next_splits():
        print(split)