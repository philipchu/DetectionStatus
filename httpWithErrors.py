import requests


def getE(url, json={}, params={}):
    try:
        requests.get(url, params=params, json=json)
    except requests.exceptions.RequestException as e:
        SystemExit(e)


def postE(url, json={}, params={}, headers={}):
    try:
        requests.post(url, params=params, json=json, headers=headers)
    except requests.exceptions.RequestException as e:
        SystemExit(e)


# def sendE(session, request):
#     try:
#         session.send(request)
#     requests.exceptions.RequestException as e:
#         SystemExit(e)
