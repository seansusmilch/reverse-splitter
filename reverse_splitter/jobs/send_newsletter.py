from jinja2 import Environment, PackageLoader, select_autoescape, DebugUndefined
from datetime import datetime, timedelta
from reverse_splitter.bin import logger, brevo, db
import os
import reverse_splitter.bin.price as price

log = logger.setup_logger('SendNewsletter')

env = Environment(
    loader=PackageLoader("reverse_splitter"),
    undefined=DebugUndefined,
    autoescape=select_autoescape()
)

NEWSLETTER_MIN_DAYS = int(os.environ.get('NEWSLETTER_MIN_DAYS', 5))
NEWSLETTER_MAX_DAYS = int(os.environ.get('NEWSLETTER_MAX_DAYS', 14))
NEWSLETTER_MIN_SPLIT_COUNT = int(os.environ.get('NEWSLETTER_MIN_SPLIT_COUNT', 3))

def create_newsletter(splits):
    date_string = datetime.today().strftime('%B %d, %Y')
    
    last_prices = price.get_last_prices([split.stock for split in splits])
    for split in splits:
        split.last_price = last_prices[split.stock]
    
    template = env.get_template('newsletter.html')
    rendered = template.render(splits=splits, date=date_string)
    
    return {
        'date': datetime.today().strftime('%Y-%m-%d'),
        'subject': f'[{datetime.today().strftime('%m-%d')}] Reverse Splitter Newsletter',
        'content': rendered
    }

def send_newsletter_job():
    newsletter_max_date = datetime.today() + timedelta(days=NEWSLETTER_MAX_DAYS)
    newsletter_max_date_string = newsletter_max_date.strftime('%Y-%m-%d')
    reverse_splits = db.get_pb().collection('reverse_splits')
    unsent_splits = reverse_splits.get_full_list(
        query_params={
            'filter': f'campaign_id = 0 && effective_date <= "{newsletter_max_date_string}"', 'sort': 'effective_date'
            }
        )
    
    if not unsent_splits:
        log.debug('No unsent splits')
        return
    
    newsletter_min_date = datetime.today() + timedelta(days=NEWSLETTER_MIN_DAYS)
    newsletter_min_date_string = newsletter_min_date.strftime('%Y-%m-%d')
    
    first_split_is_soon = unsent_splits[0].effective_date <= newsletter_min_date_string
    enough_splits = len(unsent_splits) > NEWSLETTER_MIN_SPLIT_COUNT
    
    if not first_split_is_soon and not enough_splits:
        log.debug('Not enough splits to send newsletter')
        return
    
    log.debug(f'Creating newsletter for reason first_split_is_soon={first_split_is_soon} enough_splits={enough_splits}')
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
    send_newsletter_job()
    # newsletter_max_date = datetime.today() + timedelta(days=NEWSLETTER_MAX_DAYS)
    # newsletter_max_date_string = newsletter_max_date.strftime('%Y-%m-%d')
    # reverse_splits = db.get_pb().collection('reverse_splits')
    # res = reverse_splits.get_full_list(
    #     query_params={
    #         'filter': f'campaign_id = 0 && effective_date <= "{newsletter_max_date_string}"', 'sort': 'effective_date'
    #         }
    #     )
    
    # print(vars(res[0]))