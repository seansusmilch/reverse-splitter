import reverse_splitter.bin.find_press_release as press_finder
import reverse_splitter.bin.split_calendar as calendar
import reverse_splitter.bin.gemini_summarizer as summarizer
import reverse_splitter.bin.db as db
import reverse_splitter.bin.logger as logger

log = logger.setup_logger('Research')

def research_job():
    upcoming_splits = calendar.get_next_splits()
    
    for split in upcoming_splits:
        try:
            # Check if record already exists
            db.get_pb().collection('reverse_splits').get_first_list_item(f'stock = "{split[0]}" && effective_date = "{split[4]}"')
            log.debug(f'Record for {split[0]} on {split[4]} already exists')
            continue
        except:
            # No record found
            pass
        
        press = press_finder.find_press_release(f'{split[0]} reverse split press release')
        if not press:
            log.warning(f'No press release found for {split[0]} on {split[4]}')
            return
        
        real_url, article = press
        summary = summarizer.summarize_article(article)
        
        split_record = {
            'stock': split[0],
            'exchange': split[1],
            'company_name': split[2],
            'split_ratio': split[3],
            'effective_date': split[4],
            'press_release': real_url,
            'summary': summary,
            'sent': False
        }
    
        db.get_pb().collection('reverse_splits').create(split_record)



if __name__ == '__main__':
    research_job()