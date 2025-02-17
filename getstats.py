import requests

def get_storage(ip):
    req = requests.get('http://'+ip+'/info')
    full = 0
    total = 0
    for i in req.json()['storage']:
        total += i['size']
    req = requests.get('http://' + ip + '/load/storage')
    for i in req.json():
        full += i
    return 100*full/total

def get_ram(ip):
    req = requests.get('http://'+ip+'/info')
    total = req.json()['ram']['size']
    req = requests.get('http://' + ip + '/load/ram')
    full = req.json()['load']
    return 100*full/total
