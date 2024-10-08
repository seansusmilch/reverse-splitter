import reverse_splitter.bin.split_calendar.yahoo as yahoo
import reverse_splitter.bin.split_calendar.hedgefollow as hedgefollow
import reverse_splitter.bin.split_calendar.briefing as briefing
from datetime import datetime

def get_next_splits():
    '''
    Format: ['RYAAY', 'NASDAQ', 'Ryanair Holdings plc', '5:2', '2024-09-30', '2024-09-13']
    
    Need to:
    - Filter for reverse splits
    - Filter stock exchange (NASDAQ or NYSE)
    - Filter splits within the next x days
    '''
    # make set to filter out duplicates
    hedge = hedgefollow.scrape_hedgefollow()
    brief = briefing.scrape_briefing()
    hoo = yahoo.scrape_yahoo()
    all_splits = set().union(hedge, brief, hoo)
    
    reverse_splits = list(filter(lambda split: split.ratio.startswith('1:') or split.ratio.startswith('1.00 -'), all_splits))
    
    exchange_blacklist = ['OTC']
    reverse_splits = list(filter(lambda split: split.exchange not in exchange_blacklist, reverse_splits))
    
    reverse_splits = list(filter(lambda split: datetime.today() <= datetime.strptime(split.effective_date, '%Y-%m-%d'), reverse_splits))
    
    reverse_splits = sorted(reverse_splits, key=lambda split: datetime.strptime(split.effective_date, '%Y-%m-%d'))
    
    return reverse_splits



if __name__ == '__main__':
    for split in get_next_splits():
        print(split)
        pass