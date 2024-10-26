import reverse_splitter.bin.find_press_release as press_finder
import reverse_splitter.bin.split_calendar as calendar
import reverse_splitter.bin.gemini_summarizer as summarizer
import reverse_splitter.bin.db as db
import reverse_splitter.bin.logger as logger

log = logger.setup_logger('Research')

def research_job():
    upcoming_splits = calendar.get_next_splits()
    
    log.info(f'Processing {len(upcoming_splits)} upcoming reverse splits')
    for split in upcoming_splits:
        try:
            # Check if record already exists
            db.get_pb().collection('reverse_splits').get_first_list_item(f'stock = "{split.ticker}" && effective_date = "{split.effective_date}"')
            log.debug(f'Skipping {split.ticker} on {split.effective_date}: already exists')
            continue
        except:
            # No record found
            pass
        
        press = press_finder.find_press_release(f'"{split.ticker}" reverse split press release "fractional"')
        if not press:
            log.warning(f'No press release found for {split.ticker} on {split.effective_date}')
            return
        
        real_url, article = press
        summary = summarizer.summarize_article(article)
        log.debug(f'Summary for {split.ticker} on {split.effective_date} - "{summary[0:10]}..."')
        
        split_record = {
            'stock': split.ticker,
            'exchange': split.exchange,
            'company_name': split.company_name,
            'split_ratio': split.ratio,
            'effective_date': split.effective_date,
            'press_release': real_url,
            'summary': summary,
        }
    
        db.get_pb().collection('reverse_splits').create(split_record)
        log.info(f'Record for {split.ticker} on {split.effective_date} created')



if __name__ == '__main__':
    research_job()