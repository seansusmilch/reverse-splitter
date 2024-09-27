from urllib3.util import parse_url
from urllib.parse import unquote

def get_real_url(raw_url):
    parsed_url = parse_url(raw_url)
    paths = parsed_url.path.split('/')
    for element in paths:
        if element.startswith('RU='):
            return unquote(element).replace('RU=', '')
        
        
if __name__ == '__main__':
    url = 'https://r.search.yahoo.com/_ylt=AwrhWOwRyPVmy68EjuZXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Ny/RV=2/RE=1728593170/RO=10/RU=https%3a%2f%2fwww.morningstar.com%2fnews%2fbusiness-wire%2f20240920380774%2fshiftpixy-inc-announces-reverse-stock-split-effective-date/RK=2/RS=EzsWSwIPi4oC47yLE5Zd6CAYCXQ-'
    print(get_real_url(url))