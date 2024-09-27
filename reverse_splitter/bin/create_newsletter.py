from jinja2 import Environment, PackageLoader, select_autoescape, DebugUndefined
from datetime import datetime
import reverse_splitter.bin.db as db

env = Environment(
    loader=PackageLoader("reverse_splitter"),
    undefined=DebugUndefined,
    autoescape=select_autoescape()
)

def create_newsletter(splits):
    date_string = datetime.today().strftime('%B %d, %Y')
    
    template = env.get_template('newsletter.html')
    rendered = template.render(splits=splits, date=date_string)
    
    return db.get_pb().collection('newsletters').create({
        'date': datetime.today().strftime('%Y-%m-%d'),
        'subject': f'[{datetime.today().strftime('%m-%d')}] Reverse Splitter Newsletter',
        'content': rendered
    })


if __name__ == '__main__':
    print(create_newsletter([
        {
            'stock': 'RYAAY',
            'exchange': 'NASDAQ',
            'company_name': 'Ryanair Holdings plc',
            'split_ratio': '5:2',
            'effective_date': '2024-09-30',
            'press_release': 'https://www.ryanair.com/press-release',
            'summary': 'Ryanair Holdings plc announced a 5:2 reverse split on September 30, 2024. The split will be effective on September 30, 2024. Read more at https://www.ryanair.com/press-release',
            'sent': False
        }
    ]))