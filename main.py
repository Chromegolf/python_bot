import requests
from bs4 import BeautifulSoup

#const
url = 'https://www.avito.ru/pik-arenda/moskva/kvartiry/sdam' 
user_headers = {
    'User-agent': '(Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Accept': '*/*'
}
host = 'https://www.avito.ru'

def get_html(url, params=None):
    req = requests.get(url, headers=user_headers, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item item_table clearfix js-catalog-item-enum')
    
    apartment = []
    for item in items:
        metro_station = item.find('i', class_='i-metro i-metro-msk-2')
        address = item.find('p', class_='address').get_text(strip=True)
        if metro_station:
            metro_station = metro_station.get_text() + address
        else:
            metro_station = address

        apartment.append({
            'title': item.find('a', class_='item-description-title-link').get_text(strip=True),
            'address': metro_station,       
            'price': item.find('span', class_='price').get('content') + ' руб',
            'commision': item.find('span', class_='about__commission').get_text(strip=True),
            'link': host + item.find('a', class_='item-description-title-link').get('href'),
            'date': item.find('div', class_='data').find_next('div', class_='js-item-date c-2').get_text(strip=True)
        })
    print (apartment)
    return apartment

def parse():
    html = get_html(url)
    if html.status_code == 200:
        apartment = get_content(html.text)
    else:
        print('Error on get page')

parse()

#item__line
#item_table-wrapper 
#description item_table-description
#title item-description-title
#item-description-title-link
#name
