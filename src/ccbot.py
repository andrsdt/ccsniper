import requests
import json
import messages
from bs4 import BeautifulSoup as soup



def fetchProduct(url,keywords):

    found = False

    response = requests.get(url = url)
    if response.status_code != 200:
        print('The http request couldn\'t be processed.')

    html_soup = soup(response.text, 'html.parser')
    product_frames = html_soup.find_all('div', class_ = 'col-sm-6 col-lg-4 col-xl-3')
    products = [p.find_all('div', class_ = 'box-product tiles-container')[0] for p in product_frames]

    products_dicc = {json.loads(p.a['data-dl'])['name']:
                    [
                    json.loads(p.a['data-dl'])['price'],
                    json.loads(p.a['data-dl'])['url']] for p in products}

    for p in products_dicc:
        for k in keywords:
            if k.lower() in p.lower():
                name = p
                found = True
                price = f'{products_dicc[p][0]}€'
                matching_keyword = k
                final_url = f'https://www.cashconverters.es{products_dicc[p][1]}'
    
    return [found,name,price,final_url,matching_keyword]

