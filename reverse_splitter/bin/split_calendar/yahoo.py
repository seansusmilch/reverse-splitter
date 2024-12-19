import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime, timedelta
import cachetools.func
from reverse_splitter.bin.types import Split
from typing import List
import os
import reverse_splitter.bin.logger as logger

log = logger.setup_logger("Yahoo")


@cachetools.func.ttl_cache(maxsize=1, ttl=3600)
def get_symbols_index():
    print("Getting symbols index")
    url = "https://files.catnmsplan.com/symbol-master/FINRACATReportableEquitySecurities_Intraday.txt"
    res = requests.get(url)
    lines = res.text.split("\n")
    non_tests = [line for line in lines if not line.endswith("|Y")]

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

    exchanges = ["A", "N", "Q"]
    split = [line.split("|") for line in non_tests]
    correct_length = [line for line in split if len(line) == 4]
    correct_exchange = [row for row in correct_length if row[2] in exchanges]

    return correct_exchange


def get_symbol_from_index(symbol):
    """Symbol, Company Name, Exchange"""
    index = get_symbols_index()
    symbol_row = next((row for row in index if row[0] == symbol), None)
    if not symbol_row:
        return

    exchange_map = {
        "A": "NYSE",
        "N": "NYSE",
        "Q": "NASDAQ",
    }
    symbol_info = {
        "symbol": symbol_row[0],
        "company_name": symbol_row[1],
        "exchange": exchange_map[symbol_row[2]],
    }
    return symbol_info


async def get_raw_data(start_day=datetime.today()) -> List[Split]:
    """Need to start on a sunday"""
    calendar_selector = ".calendar.week"
    days_selector = f"{calendar_selector} > div.container > div.item > a"
    table_selector = "main > .table-container > table"
    all_table_data = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=os.name != "nt")
        context = await browser.new_context()
        page = await context.new_page()

        # TODO: This will also get previous splits that I don't want
        await page.goto(
            f"https://finance.yahoo.com/calendar/splits?day={start_day.strftime('%Y-%m-%d')}",
            wait_until="commit",
        )
        await page.wait_for_selector(calendar_selector)

        clickable_days = len(await page.query_selector_all(days_selector))

        for idx in range(clickable_days):
            previous_url = page.url
            await (await page.query_selector_all(days_selector))[idx].click()
            await page.wait_for_function(
                "(prev_url) => window.location.href !== prev_url", arg=previous_url
            )
            await page.wait_for_selector(table_selector)

            parsed_url = urlparse(page.url)
            day_param = parse_qs(parsed_url.query).get("day", [None])[0]

            table = await page.query_selector(table_selector)
            tableData = await table.evaluate(
                "(tbl) => [...tbl.rows].map(r => [...r.cells].map(c => c.textContent))"
            )

            # ['Symbol', 'Company', 'Payable on', 'Optionable?', 'Ratio']
            for row in tableData:
                if len(row) != 5:
                    continue
                symbol_info = get_symbol_from_index(row[0].strip())
                if not symbol_info:
                    continue

                symbol = row[0].strip()
                company_name = row[1].strip()
                exchange = symbol_info["exchange"].strip()
                effective_date = day_param
                ratio = row[4].strip()

                all_table_data.append(
                    [symbol, exchange, company_name, ratio, effective_date]
                )

        await browser.close()

    return [Split(*split) for split in all_table_data]


def get_sundays(today=datetime.today()):
    sunday = (
        today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
    )
    next_sunday = sunday + timedelta(days=7)
    return sunday.date(), next_sunday.date()


async def scrape_yahoo() -> List[Split]:
    try:
        all_splits = []
        for sunday in get_sundays():
            all_splits += await get_raw_data(sunday)
            log.debug(f"Got data for the week of {sunday}")

        reverse_splits = [
            split for split in all_splits if split.ratio.startswith("1.00")
        ]

        return reverse_splits
    except Exception as e:
        log.error(f"Error scraping Yahoo: {e}", exc_info=True)
        return []


if __name__ == "__main__":
    for split in asyncio.run(scrape_yahoo()):
        print(split)
