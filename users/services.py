import requests
import json
from django.shortcuts import get_object_or_404
from materials.models import Stripe
from django.conf import settings



def create_product(name, headers):
    '''формируем данные для POST-запроса в Stripe, чтобы создать продукт'''
    url = 'https://api.stripe.com/v1/products'
    headers = headers
    params = {'name': name}
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_product = json.loads(response.text)
    return stripe_product


def create_price(product_id, headers):
    '''формируем данные для POST-запроса в Stripe, чтобы создать стоимость'''
    url = 'https://api.stripe.com/v1/prices'
    headers = headers
    params = {'currency': 'usd', 'unit_amount': 1000, 'product': product_id}   #'recurring[interval]': 'month',
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_price = json.loads(response.text)
    return stripe_price


def create_session(course_id, headers):
    '''формируем данные для POST-запроса в Stripe, чтобы создать сессию для получения ссылки на оплату'''
    stripe_data = get_object_or_404(Stripe, course_id=course_id)
    stripe_price = stripe_data.stripe_price
    #print(f'прайс из таблицы Stripe:   {stripe_price}')          #для отладки
    url = 'https://api.stripe.com/v1/checkout/sessions'
    headers = headers
    params = {'line_items[0][price]': stripe_price,
              'line_items[0][quantity]': 1, 'mode': 'payment', #'mode': 'subscription',
              'success_url': 'https://example.com/success'}
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_link = json.loads(response.text)
    #print(stripe_link['url'])      #для отладки
    return stripe_link['url']


