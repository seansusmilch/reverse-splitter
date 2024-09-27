from jinja2 import Environment, PackageLoader, select_autoescape, DebugUndefined
import reverse_splitter.bin.emailer as emailer
import reverse_splitter.bin.db as db
import reverse_splitter.bin.logger as logger

env = Environment(
    loader=PackageLoader("reverse_splitter"),
    undefined=DebugUndefined,
    autoescape=select_autoescape()
)

log = logger.setup_logger('Welcome')

def send_welcome_job():
    new_subscribers = db.get_pb().collection('subscribers').get_full_list(query_params={'filter': 'welcomed = false'})
    
    if not new_subscribers:
        log.debug('No new subscribers')
        return
    
    template = env.get_template('welcome.html')
    for sub in new_subscribers:
        if 'seantsusmilch' not in sub.email: continue
        name = sub.name
        email = sub.email
        unsubscribe_link=f'https://reverse-splitter.vercel.app/unsubscribe?code={sub.id}'
        
        hydrated_content = template.render(name=name, unsubscribe_link=unsubscribe_link)
        
        log.debug(f'Sending welcome email to {name} {email}')
        emailer.send_html_email(email, 'Welcome to Reverse Splitter', hydrated_content)
        
        log.debug(f'Updating subscriber welcomed status {sub.id}')
        db.get_pb().collection('subscribers').update(sub.id, {'welcomed': True})
        
        
        
if __name__ == '__main__':
    send_welcome_job()