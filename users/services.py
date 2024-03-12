import requests
import json
#import stripe

def create_product(name):
    '''формируем данные для POST-запроса в Stripe, чтобы создать продукт'''
    url = 'https://api.stripe.com/v1/products'
    headers = {'Authorization': 'Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection': 'keep-alive'}
    params = {'name': name}
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_product = json.loads(response.text)
    return stripe_product


def create_price(product_id):
    '''формируем данные для POST-запроса в Stripe, чтобы создать стоимость'''
    url = 'https://api.stripe.com/v1/prices'
    headers = {'Authorization': 'Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection': 'keep-alive'}
    params = {'currency': 'rub', 'unit_amount': 1000, 'recurring[interval]': 'month', 'product': product_id}
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_price = json.loads(response.text)
    return stripe_price


def create_session():
    '''формируем данные для POST-запроса в Stripe, чтобы создать сессию для получения ссылки на оплату'''
    response = requests.post('https://stripe.com/docs/api/checkout/sessions/create')
    print(response.status_code)
    print(response.text)


