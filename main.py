import requests
from bs4 import BeautifulSoup

from config import URL
from config import HOST
from config import USER_HEADERS

def get_html(url, params=None):
    params = {
        'pmin': 20000,
        'pmax': 25000
    }
    req = requests.get(URL, headers=USER_HEADERS, params=params)
    return req

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0] 
    except:    
        total_pages = 1

    return int(total_pages)
    
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
            'Квартира': item.find('a', class_='item-description-title-link').get_text(strip=True),
            'Адрес': metro_station,       
            'Стоимость': item.find('span', class_='price').get('content') + ' руб',
            'Коммиссия': item.find('span', class_='about__commission').get_text(strip=True),
            'Опубликовано': item.find('div', class_='data').find_next('div', class_='js-item-date c-2').get_text("|", strip=True),
            'link': HOST + item.find('a', class_='item-description-title-link').get('href'),
        })  
    return ('\n'.join(map(str, apartment)))
    #return apartment

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        apartments = []
        pages_count = get_total_pages(html.text)

        if pages_count > 1:
            for page in range(1, pages_count + 1):
                print(f'Parse process, page is {page} of {pages_count}...')
                html = get_html(URL, params={'page': page})
                apartments.extend(get_content(html.text))
        else:
            apartments = get_content(html.text)      

    else:
        print('Error on get page')
    return apartments

#parse()
