import requests


def get_proxy():
    try:
        return requests.get("http://127.0.0.1:5010/get/").json()['proxy']
    except ConnectionError as e:
        return '127.0.0.1'


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
