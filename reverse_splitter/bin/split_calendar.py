# https://hedgefollow.com/upcoming-stock-splits.php
import os
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def scrape_hedgefollow():
    '''['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']'''
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=os.name != 'nt')
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://hedgefollow.com/upcoming-stock-splits.php', wait_until='domcontentloaded')

    # Get the table
    table = page.query_selector('table#latest_splits')
    tableData = table.evaluate('(tbl) => [...tbl.rows].map(r => [...r.cells].map(c => c.textContent))')

    browser.close()
    playwright.stop()
        
    return tableData

def get_next_splits():
    '''
    Format: ['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']
    
    Need to:
    - Filter for reverse splits
    - Filter stock exchange (NASDAQ or NYSE)
    - Filter splits within the next x days
    '''
    data = scrape_hedgefollow()
    data = list(filter(lambda row: len(row) == 6, data)) # Remove rows that show tips
    
    reverse_splits = list(filter(lambda row: row[3].startswith('1:'), data))
    
    stock_exchanges = ['NASDAQ', 'NYSE']
    reverse_splits = list(filter(lambda row: row[1] in stock_exchanges, reverse_splits))
    
    # soon = datetime.today() + timedelta(days=4)
    # reverse_splits = list(filter(lambda row: datetime.today() <= datetime.strptime(row[4], '%Y-%m-%d') <= soon, reverse_splits))
    reverse_splits = list(filter(lambda row: datetime.today() <= datetime.strptime(row[4], '%Y-%m-%d'), reverse_splits))
    
    return reverse_splits



if __name__ == '__main__':
    print(get_next_splits())