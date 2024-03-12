import requests
import json
from django.shortcuts import get_object_or_404
from materials.models import Stripe

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
    params = {'currency': 'rub', 'unit_amount': 1000, 'product': product_id}   #'recurring[interval]': 'month',
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    stripe_price = json.loads(response.text)
    return stripe_price


def create_session(course_id):
    '''формируем данные для POST-запроса в Stripe, чтобы создать сессию для получения ссылки на оплату'''
    stripe_data = get_object_or_404(Stripe, course_id=course_id)
    stripe_price = stripe_data.stripe_price
    #print(f'прайс из таблицы Stripe:   {stripe_price}')          #для отладки
    url = 'https://api.stripe.com/v1/checkout/sessions'
    headers = {'Authorization': 'Basic c2tfdGVzdF80ZUMzOUhxTHlqV0Rhcmp0VDF6ZHA3ZGM6',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection': 'keep-alive'}
    params = {'line_items[0][price]': stripe_price,
              'line_items[0][quantity]': 1, 'mode': 'subscription', 'success_url': 'https://example.com/success'}
    response = requests.post(url=url, headers=headers, params=params)
    print(response.status_code)
    print(response.text)
    stripe_link = json.loads(response.text)
    return stripe_link


