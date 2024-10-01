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
    
    welcome_template_id = db.get_user().welcome_template_id
        
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
        else:
            log.info(f'Added subscriber {name} ({email}) to Brevo')
        
        if welcome_template_id != 0:
            log.debug(f'Sending welcome email to {name} ({email})')
            brevo.send_transactional(welcome_template_id, to=[{'email': email, 'name': name}])

    
if __name__ == '__main__':
    add_new_subscribers_job()
    