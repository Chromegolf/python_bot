import requests
import logging

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

from config import URL
from config import HOST
from config import USER_HEADERS


def get_html(url, params=None):
    params = {
        'pmin': 30000,
        'pmax': 40000
    }
    req = requests.get(URL, headers=USER_HEADERS, params=params)
    return req


def get_total_pages(html):
    soup = BeautifulSoup(html, 'html5lib')

    try:
        pages = soup.find('div', class_='b-shop-pagination').find_next('div',
                                                                       class_='pagination-pages clearfix').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0]
    except:
        total_pages = 1

    return int(total_pages)


def get_content(html):
    soup = BeautifulSoup(html, 'html5lib')
    try:
        # получаем контент со страницы в указанном div
        items_page = soup.find_all(
            'div', class_='item item_table clearfix js-catalog-item-enum')
        logging.debug('find div with items')
    except:
        logging.debug('Could not find div with items')

    apartment = []

    # TODO:добавить логи
    for item in items_page:
        # div блок где хранится адреса объявления
        find_address_div = item.find_next('div', class_='item-address')
        # div блок где хранится информация о метро
        metro_div = find_address_div.find_next(
            # ищем все span в div блоке
            'div', class_='item-address-georeferences').find_all('span')

        if find_address_div:
            # сохраняем адрес полный почтовый адрес
            full_address = find_address_div.find_next(
                "span", class_="item-address__string").get_text(strip=True)
            # если в div есть span блоки
            if metro_div:
                metro_station = find_address_div.find_next(
                    'div', class_='item-address-georeferences').find_next('span', class_='item-address-georeferences').find_next(
                    'span', class_='item-address-georeferences-item__content').get_text(strip=True)
                metro_distance = find_address_div.find_next(
                    'div', class_='item-address-georeferences').find_next('span', class_='item-address-georeferences').find_next(
                    'span', class_='item-address-georeferences-item__after').get_text(strip=True)

                metro_info = 'м.' + metro_station + '-' + metro_distance
                metro_info = metro_info.replace(u'\xa0', ' ')

            else:
                metro_info = 'Рядом метро нет'
        else:
            print('Could not find div')

        apartment.append({
            'Квартира': item.find('a', class_='item-description-title-link').get_text(strip=True),
            'Адрес': metro_info + ', ' + full_address,
            'Стоимость': item.find('span', class_='price').get('content') + ' руб',
            'Коммиссия': item.find('span', class_='about__commission').get_text(strip=True),
            'Опубликовано': item.find('div', class_='data').find_next('div', class_='js-item-date c-2').get_text("|", strip=True),
            'link': HOST + item.find('a', class_='item-description-title-link').get('href'),
        })
    return ('\n'.join(map(str, apartment)))
    # return apartment


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
