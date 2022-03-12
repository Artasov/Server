from datetime import datetime, timedelta
import os
import requests


def create_bill(value, product, license_time, billid, username):
    SECRET_KEY = os.getenv('QIWI_SECRET_KEY')
    now = datetime.now()
    ex_date = now + timedelta(minutes=10)

    headers = {'Authorization': f'Bearer {SECRET_KEY}',
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Referrer-Policy': 'localhost'}

    params = {'amount': {'value': value,
                         'currency': 'RUB'},
              'comment': f'Product: {product}  |  License time: {license_time.replace("price_", "")} | {username}',
              'expirationDateTime': f'{ex_date.strftime("%Y-%m-%dT%H:%MZ")}',
              'customer': {},
              'customFields': {'product': product,
                               'license_time': license_time},
              }

    g = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{billid}',
                     headers=headers,
                     json=params)
    return g.json()


def check_bill(billid):
    SECRET_KEY = os.getenv('QIWI_SECRET_KEY')
    headers = {'Authorization': f'Bearer {SECRET_KEY}',
               'Accept': 'application/json'}

    g = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{billid}',
                     headers=headers)
    return g.json()


def del_bill(billid):
    SECRET_KEY = os.getenv('QIWI_SECRET_KEY')
    headers = {'Authorization': f'Bearer {SECRET_KEY}',
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    g = requests.post(f'https://api.qiwi.com/partner/bill/v1/bills/{billid}/reject',
                      headers=headers)
    return g.json()

