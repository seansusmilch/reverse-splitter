import reverse_splitter.bin.emailer as emailer
import reverse_splitter.bin.db as db
import reverse_splitter.bin.create_newsletter as news
from jinja2 import Environment, PackageLoader, select_autoescape, DebugUndefined

env = Environment(
    loader=PackageLoader("reverse_splitter"),
    undefined=DebugUndefined,
    autoescape=select_autoescape()
)


def send_newsletter_job():
    unsent_splits = db.get_pb().collection('reverse_splits').get_full_list(query_params={'filter': 'sent = false', 'sort': 'effective_date'})
    
    if not unsent_splits:
        print('No unsent splits')
        return
    
    newsletter_record = news.create_newsletter(unsent_splits)
    subject = newsletter_record.subject
    content = newsletter_record.content
    template = env.from_string(content)
    
    for split in unsent_splits:
        print('Updating split sent status', split.id)
        db.get_pb().collection('reverse_splits').update(split.id, {'sent': True})
        
    
    subscribers = db.get_pb().collection('subscribers').get_full_list()
    for subscriber in subscribers:
        name = subscriber.name
        email = subscriber.email
        unsubscribe_link=f'https://reverse-splitter.vercel.app/unsubscribe?code={subscriber.id}'
        
        hydrated_content = template.render(name=name, unsubscribe_link=unsubscribe_link)
        
        print('Sending email to', name, email)
        emailer.send_html_email(email, subject, hydrated_content)
        

if __name__ == '__main__':
    send_newsletter_job()