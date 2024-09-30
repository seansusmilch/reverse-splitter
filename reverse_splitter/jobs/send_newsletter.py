from jinja2 import Environment, PackageLoader, select_autoescape, DebugUndefined
from datetime import datetime, timedelta
from reverse_splitter.bin import logger, brevo, db
import os

log = logger.setup_logger('SendNewsletter')

env = Environment(
    loader=PackageLoader("reverse_splitter"),
    undefined=DebugUndefined,
    autoescape=select_autoescape()
)

NEWSLETTER_MIN_DAYS = os.environ.get('NEWSLETTER_MIN_DAYS', 5)
NEWSLETTER_MIN_SPLIT_COUNT = os.environ.get('NEWSLETTER_MIN_SPLIT_COUNT', 3)

def create_newsletter(splits):
    date_string = datetime.today().strftime('%B %d, %Y')
    
    template = env.get_template('newsletter.html')
    rendered = template.render(splits=splits, date=date_string)
    
    return {
        'date': datetime.today().strftime('%Y-%m-%d'),
        'subject': f'[{datetime.today().strftime('%m-%d')}] Reverse Splitter Newsletter',
        'content': rendered
    }

def send_newsletter_job():
    reverse_splits = db.get_pb().collection('reverse_splits')
    unsent_splits = reverse_splits.get_full_list(query_params={'filter': 'campaign_id = 0', 'sort': 'effective_date'})
    
    if not unsent_splits:
        log.debug('No unsent splits')
        return
    
    newsletter_min_date = datetime.today() + timedelta(days=NEWSLETTER_MIN_DAYS)
    newsletter_min_date_string = newsletter_min_date.strftime('%B %d, %Y')
    
    first_split_is_soon = unsent_splits[0].effective_date <= newsletter_min_date_string
    enough_splits = len(unsent_splits) < NEWSLETTER_MIN_SPLIT_COUNT
    
    if not first_split_is_soon and not enough_splits:
        log.debug('Not enough splits to send newsletter')
        return
    
    newsletter = create_newsletter(unsent_splits)
    subject = newsletter['subject']
    content = newsletter['content']
        
    campaign_id, err = brevo.create_campaign(subject, subject, content)
    if err:
        log.error(f'Error creating campaign: {err}')
        return
    
    for split in unsent_splits:
        log.debug(f'Sending split {split.id} {split.stock} in campaign {campaign_id}')
        reverse_splits.update(split.id, {'campaign_id': campaign_id})
    
    brevo.send_campaign(campaign_id)
    log.info(f'Sent {len(unsent_splits)} splits in campaign {campaign_id}')
    
    db.get_pb().collection('users').update(db.get_user().id, {'latest_campaign_id': campaign_id})
    
if __name__ == '__main__':
    # send_newsletter_job()
    reverse_splits = db.get_pb().collection('reverse_splits')
    unsent_splits = reverse_splits.get_full_list(query_params={'sort': 'effective_date'})
    for split in unsent_splits:
        print(vars(split))