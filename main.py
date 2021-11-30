from builtins import min

import requests
import json
from datetime import date
import time
import numpy as np
from termcolor import colored


def request(origin_lat, origin_long, dest_lat, dest_long):
    try:
        headers = {
            'authority': 'app.snapp.taxi',
            'content-type': 'application/json',
            'x-app-name': 'passenger-pwa',
            'x-app-version': '5.0.1',
            'authorization': 'ENTER YOUR AUTH KEY',
            'locale': 'fa-IR',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36',
            'app-version': 'pwa',
            'accept': '*/*',
            'origin': 'https://app.snapp.taxi',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.snapp.taxi/pre-ride?utm_source=website&utm_medium=webapp-button',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'cookie': '_ga=GA1.2.630158201.1604921803; _gid=GA1.2.2129247538.1605042565; facb35cfb204e400bdbaa82b44a500a9=9061bb9db340faf4174fe4745d27fc7b; 34b7ed1b00e796d0bcdc387e62021f03=acd89f353aefff86ad7cc9f6453e7a39',
        }

        data = '{"origin_lat":' + str(origin_lat) + ',"origin_lng":' + str(origin_long) + ',"destination_lat":' + str(
            dest_lat) + ',"destination_lng":' + str(
            dest_long) + ',"waiting":null,"tag":0,"round_trip":false,"voucher_code":null}'

        response = requests.post('https://app.snapp.taxi/api/api-base/v2/passenger/price/s/6/0', headers=headers,
                                 data=data)

        data = json.loads(response.content)
        data = data["data"]
        service = data['prices']
        m = int(10000000000000)
        for serv in service:
            final = int(serv['final'])
            m = int(np.min([m, final]))
            return m
        write_in_file(m)
    except:
        print(colored('something wrong', 'red'))
        write_in_file('something wrong')


def write_in_file(price):
    fi = open("snapp.csv", 'a')
    fi.write(str(price) + ' , ' + str(date.today()) + ' , ' + str(time.strftime("%H:%M:%S", time.localtime())))
    fi.write('\n')
    fi.close()


if __name__ == '__main__':
    print(time.strftime("%H:%M:%S", time.localtime()))
    res = 100000000
    price_list = []
    origin_lat = 35.7992
    origin_long =51.4075
    dest_lat =35.7114
    dest_long = 51.407
    step = .0005
    res_origin_lat = origin_lat
    res_origin_long = origin_long
    res_dest_long = dest_long
    res_dest_lat = dest_lat

    for a in range(-500, 500, 100):
        for b in range(-500, 500, 50):
            lat = origin_lat + round(a * .00001, 4)
            long = origin_long + round(a * .00001, 4)
            price = request(lat, long, dest_lat , dest_long)
            res = min(price, res)
            if price == res:
                res_lat = lat
                res_long = long
            price_list.append(price)


    for a in range(-500, 500, 100):
        for b in range(-500, 500, 50):
            lat = dest_lat + round(a * .00001, 4)
            long = dest_long + round(a * .00001, 4)
            price = request(res_origin_lat, res_origin_long, lat , long)
            res = min(price, res)
            if price == res:
                res_origin_lat = lat
                res_origin_long = long
            price_list.append(price)

    print(colored(str(time.strftime("%H:%M:%S", time.localtime())), 'yellow'), colored(res, 'green'))
    print('origin location \t' + str(res_origin_lat) + ',' + str(res_origin_long))
    print('dest location \t' + str(res_dest_lat) + ',' + str(res_dest_long))
    print('max price \t' + colored(max(price_list), 'red'))
