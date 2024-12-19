# https://hedgefollow.com/upcoming-stock-splits.php

from playwright.async_api import async_playwright
from typing import List
from reverse_splitter.bin.types import Split
import os


async def scrape_hedgefollow() -> List[Split]:
    """['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']"""

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=os.name != "nt")
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(
            "https://hedgefollow.com/upcoming-stock-splits.php",
            wait_until="domcontentloaded",
        )

        # Get the table
        table = await page.wait_for_selector("table#latest_splits")
        # Wait for the table to load
        await page.wait_for_selector("table#latest_splits tbody tr")
        rawTableData = await table.evaluate(
            "(tbl) => [...tbl.rows].map(r => [...r.cells].map(c => c.textContent))"
        )

        await browser.close()

    tableData = list(filter(lambda row: len(row) == 6, rawTableData))

    splits = []
    for row in tableData:
        splits.append(Split(row[0], row[1], row[2], row[3], row[4]))

    return splits


if __name__ == "__main__":
    import asyncio

    for split in asyncio.run(scrape_hedgefollow()):
        print(split)
        pass
