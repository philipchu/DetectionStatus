import requests


def getE(url, json={}, params={}):
    try:
        resp = requests.get(url, params=params, json=json)
        return resp
    except requests.exceptions.RequestException as e:
        SystemExit(e)


def postE(url, json={}, params={}, headers={}):
    try:
        resp = requests.post(url, params=params, json=json, headers=headers)
        return resp
    except requests.exceptions.RequestException as e:
        SystemExit(e)


# def sendE(session, request):
#     try:
#         session.send(request)
#     requests.exceptions.RequestException as e:
#         SystemExit(e)
