import brevo_python
from brevo_python.rest import ApiException
import reverse_splitter.bin.logger as logger
import os

log = logger.setup_logger('Brevo')

BREVO_API_KEY = os.getenv('BREVO_API_KEY')
BREVO_SUBSCRIBER_LIST_ID = os.getenv('BREVO_SUBSCRIBER_LIST_ID')
BREVO_SENDER_FROM_NAME = os.getenv('BREVO_SENDER_FROM_NAME')
BREVO_SENDER_FROM_EMAIL = os.getenv('BREVO_SENDER_FROM_EMAIL')

def get_client():
    if not BREVO_API_KEY:
        raise ValueError('BREVO_API_KEY is not set')
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    
    client = brevo_python.ApiClient(configuration)
    return client

def create_contact(email:str, name:str, list_ids:list=None):
    if not list_ids:
        list_ids = [int(BREVO_SUBSCRIBER_LIST_ID)]
        
    log.debug(f'Creating contact: {name} ({email})')
    
    client = get_client()
    api = brevo_python.ContactsApi(client)
    transactional = brevo_python.TransactionalEmailsApi(client)
    
    contact = brevo_python.CreateContact(
        email=email,
        attributes={'FIRSTNAME': name},
        list_ids=list_ids,
        update_enabled=True,
        email_blacklisted=False
    )
    
    
    res, err = None, None
    try:
        response = api.create_contact(contact)
        res = vars(response)['_id']
    except ApiException as e:
        log.error(f"Exception when calling ContactsApi->create_contact: {e}")
        err = e
    
    try:
        transactional.smtp_blocked_contacts_email_delete(email)
    except ApiException as e:
        pass
    
    return res, err

def create_campaign(campaign_name, subject, html_content, recipient_list_ids:list=None):
    if not recipient_list_ids:
        recipient_list_ids = [int(BREVO_SUBSCRIBER_LIST_ID)]
        
    log.debug(f'Creating campaign: {campaign_name}')
    
    api = brevo_python.EmailCampaignsApi(get_client())
    
    campaign = brevo_python.CreateEmailCampaign(
        name=campaign_name,
        subject=subject,
        html_content=html_content,
        sender={'name': BREVO_SENDER_FROM_NAME, 'email': BREVO_SENDER_FROM_EMAIL},
        recipients={'listIds': recipient_list_ids}
    )
    
    res, err = None, None
    try:
        response = api.create_email_campaign(campaign)
        res = vars(response)['_id']
    except ApiException as e:
        log.error(f"Exception when calling EmailCampaignsApi->create_email_campaign: {e}")
        err = e
    
    return res, err

def send_campaign(campaign_id: int):
    log.debug(f'Sending campaign: {campaign_id}')
    api = brevo_python.EmailCampaignsApi(get_client())
    
    res, err = None, None
    try:
        response = api.send_email_campaign_now(campaign_id=campaign_id)
        res = response
    except ApiException as e:
        log.error(f"Exception when calling EmailCampaignsApi->send_email_campaign_now: {e}")
        err = e
    
    return res, err

if __name__ == '__main__':
    print('BREVO_API_KEY:', BREVO_API_KEY)
    print('BREVO_SUBSCRIBER_LIST_ID:', BREVO_SUBSCRIBER_LIST_ID)
    print('BREVO_SENDER_FROM_NAME:', BREVO_SENDER_FROM_NAME)
    print('BREVO_SENDER_FROM_EMAIL:', BREVO_SENDER_FROM_EMAIL)
    
    contact_id, err = create_contact('seantsusmilch@proton.me', 'Sean')
    
    # campaign_id, err = create_campaign('SEND TO NEW CONTACTS TEST', 'SEND TO NEW CONTACTS TEST', '<html><body><h1>TEST</h1><p>AAAAA<a href="https://google.com">stu</a>AAAAAAAA<a href="{{ unsubscribe }}">Unsubscribe</a></p></body></html>')
    # print('campaign:', campaign_id)
    
    # send = send_campaign(campaign_id)