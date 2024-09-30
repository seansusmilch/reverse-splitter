import reverse_splitter.bin.db as db
import reverse_splitter.bin.brevo as brevo
import reverse_splitter.bin.logger as logger

log = logger.setup_logger('AddNewSubscribers')

def add_new_subscribers_job():
    new_subs = db.get_pb().collection('new_subscribers')
    new_subs_records = new_subs.get_full_list()
    
    if not new_subs_records:
        log.debug('No new subscribers')
        return
        
    for sub in new_subs_records:
        email = sub.email
        name = sub.name
        
        res, err = brevo.create_contact(email, name)
        if err:
            log.error(f'Failed to add subscriber {name} ({email}) to Brevo: {err}')
            continue
        
        new_subs.delete(sub.id)
        
        if not res:
            log.info(f'Updated subscriber {name} ({email}) in Brevo')
            continue
        
        log.info(f'Added subscriber {name} ({email}) to Brevo')
        
    log.info(f'Added {len(new_subs_records)} new subscribers to Brevo')
    
    try:
        welcome_campaign_id = db.get_user().welcome_campaign_id
        if welcome_campaign_id == 0:
            log.debug('No welcome campaign to send to new subscribers')
            return
        
        brevo.send_campaign(welcome_campaign_id)
        log.info(f'Sent welcome campaign to new subscribers')
    except Exception as e:
        log.error(f'Error sending welcome campaign to new subscribers: {e}')

    
if __name__ == '__main__':
    add_new_subscribers_job()