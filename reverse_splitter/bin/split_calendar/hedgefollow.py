# https://hedgefollow.com/upcoming-stock-splits.php

from playwright.sync_api import sync_playwright
from typing import List
from reverse_splitter.bin.types import Split
import os

def scrape_hedgefollow() -> List[Split]:
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
    
    splits = []
    for row in tableData:
        splits.append(
            Split(
                row[0], row[1], row[2], row[3], row[4]
            )
        )

    return splits