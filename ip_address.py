from flask import request
from json import load
from urllib.request import urlopen

def ip_info(addr=''):
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    # response from url(if res==None then check connection)
    data = load(res)
    if '192.168.' not in request.remote_addr:
        response = {'ip': data['ip'],
                    'city': data['city'],
                    'country': data['country'],
                    'location': data['loc']}
    else:
        response = ""
    return response

if __name__ == '__main__':
    print(ip_info('85.66.109.217'))