from bs4 import BeautifulSoup as soup
import json
import requests


def fetchProduct(url,keywords):

    found = False

    response = requests.get(url = url)
    if response.status_code != 200:
        print('The http request couldn\'t be processed.')

    html_soup = soup(response.text, 'html.parser')
    product_frames = html_soup.find_all('div', class_ = 'col-6 col-sm-6 col-md-4 col-lg-3 col-xl-4')
    products = [json.loads(p.find_all('div', class_ = 'product-tiles tiles-container redirect-link')[0].find('a')['data-dl']) for p in product_frames]

    
    products_dicc = {p['name']:[p['price'],p['url']] for p in products}

    for p in products_dicc:
        for k in keywords:
            a =  k.lower().replace('-','')
            b = p.lower().replace('-','')

            if k.lower().replace('-','') in p.lower().replace('-',''):
                name = p
                found = True
                price = f'{products_dicc[p][0]}€'
                matching_keyword = k
                final_url = f'https://www.cashconverters.es{products_dicc[p][1]}'
                break
    
    return [found,name,price,final_url,matching_keyword] if found else None
