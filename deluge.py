import requests

def getTorrents(url, password):
    session = requests.Session()

    auth = {'method': 'auth.login',
            'params': [password],
            'id': 1}

    response = session.post(url, json=auth)
    if response.json()['result']:
        get_data = {'method': 'core.get_torrents_status',
                    'params': [[], ['name','paused','state','progress','queue']],
                    'id': 1}

        response = session.post(url, json=get_data)
        return response.json()['result']