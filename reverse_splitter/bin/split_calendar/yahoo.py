from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime, timedelta
import cachetools.func
from reverse_splitter.bin.types import Split
from typing import List
import os
import reverse_splitter.bin.logger as logger

log = logger.setup_logger('Yahoo')

@cachetools.func.ttl_cache(maxsize=1, ttl=3600)
def get_symbols_index():
    print('Getting symbols index')
    url = 'https://files.catnmsplan.com/symbol-master/FINRACATReportableEquitySecurities_Intraday.txt'
    res = requests.get(url)
    lines = res.text.split('\n')
    non_tests = [line for line in lines if not line.endswith('|Y')]
    
    # Primary Listing Exchange
    # A = NYSE American
    # N = NYSE
    # O = OTCBB
    # P = NYSE ARCA
    # Q = Nasdaq
    # U = OTC Equity
    # V = IEX
    # Z = Cboe BZX
    # Else NULL
    
    exchanges = ['A', 'N', 'Q']
    split = [line.split('|') for line in non_tests]
    correct_length = [line for line in split if len(line) == 4]
    correct_exchange = [row for row in correct_length if row[2] in exchanges]
    
    return correct_exchange

def get_symbol_from_index(symbol):
    '''Symbol, Company Name, Exchange
    '''
    index = get_symbols_index()
    symbol_row = next((row for row in index if row[0] == symbol), None)
    if not symbol_row: return
    
    exchange_map = {
        'A': 'NYSE',
        'N': 'NYSE',
        'Q': 'NASDAQ',
    }
    symbol_info = {
        'symbol': symbol_row[0],
        'company_name': symbol_row[1],
        'exchange': exchange_map[symbol_row[2]]
    }
    return symbol_info

def get_raw_data(start_day=datetime.today()) -> List[Split]:
    '''Need to start on a sunday
    '''
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=os.name != 'nt')
    context = browser.new_context()
    page = context.new_page()

    # TODO: This will also get previous splits that I don't want
    page.goto(f'https://finance.yahoo.com/calendar/splits?day={start_day.strftime('%Y-%m-%d')}', wait_until='commit')
    page.wait_for_selector('#fin-cal-events')
    
    clickable_days = len(page.query_selector_all('#fin-cal-events > div > ul > li > a'))
    
    all_table_data = []
    
    for idx in range(clickable_days):
        previous_url = page.url
        page.query_selector_all('#fin-cal-events > div > ul > li > a')[idx].click()
        page.wait_for_function('(prev_url) => window.location.href !== prev_url', arg=previous_url)
        page.wait_for_selector('#cal-res-table')
        
        parsed_url = urlparse(page.url)
        day_param = parse_qs(parsed_url.query).get('day', [None])[0]
        
        table = page.query_selector('#cal-res-table table')
        tableData = table.evaluate('(tbl) => [...tbl.rows].map(r => [...r.cells].map(c => c.textContent))')
        
        # ['Symbol', 'Company', 'Payable on', 'Optionable?', 'Ratio']
        good_data = []
        for row in tableData:
            symbol_info = get_symbol_from_index(row[0])
            if not symbol_info: continue
            
            symbol = row[0]
            company_name = row[1]
            exchange = symbol_info['exchange']
            effective_date = day_param
            ratio = row[4]
            
            good_data.append([symbol, exchange, company_name, ratio, effective_date])

        
        all_table_data += good_data
    
    browser.close()
    playwright.stop()
    
    return [Split(*split) for split in all_table_data]
    
    
def get_sundays(today=datetime.today()):
    sunday = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
    next_sunday = sunday + timedelta(days=7)
    return sunday.date(), next_sunday.date()

def scrape_yahoo() -> List[Split]:
    all_splits = []
    for sunday in get_sundays():
        all_splits += get_raw_data(sunday)
        log.debug('Got data for the week of', sunday)
        
    reverse_splits = [split for split in all_splits if split.ratio.startswith('1.00')]
    
    return reverse_splits
    
if __name__ == '__main__':
    for split in scrape_yahoo():
        print(split)