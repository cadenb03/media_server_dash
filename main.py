import datetime, time, os, getstats, deluge, threading, ping
from constants import *

ip = '127.0.0.1'

url = 'http://'+ip+':8112/json'
username = 'admin'
password = 'deluge'

services = {'Jellyfin':(ip,8096), 'Jellyseer':(ip,5055),
            'Deluge':(ip,8112), 'Sonarr':(ip,8989),
            'Radarr':(ip,7878), 'Prowlarr':(ip,9696)}

available = []

downloads = []
seeds = []

storage = getstats.get_storage(ip)
ram = getstats.get_ram(ip)

print('\033[?25l',end='')
print('\033[?25l',end='')
print(Terminal.clear+Terminal.reset, end='')
#print(colors.BG.red,str(datetime.datetime.now()),colors.reset+colors.FG.red+"\ue0b4"+colors.reset,"\ntesting testing 1 2 3")

def top_bar():
    time_ = datetime.datetime.now().strftime("%I:%M:%S %p")
    date_ = datetime.datetime.now().strftime("%a, %b %d")

    red1_bg = Colors.BG.rgb(168,32,69)
    red1_fg = Colors.FG.rgb(168,32,69)

    red2_bg = Colors.BG.rgb(209,79,101)
    red2_fg = Colors.FG.rgb(209,79,101)

    grey_bg = Colors.BG.rgb(64, 64, 64)
    grey_fg = Colors.FG.rgb(64, 64, 64)

    time_bar = grey_bg+' '+ip+' '+Colors.reset+grey_fg+red1_bg+'\ue0b4'+Colors.reset+red1_bg+' '+time_+' '+Colors.reset+red1_fg+red2_bg+'\ue0b4'+Colors.reset+red2_bg+' '+date_+' '+Colors.reset+red2_fg+'\ue0b4'+Colors.reset
    time_length = 15+len(time_)+3+len(date_)+2

    purple1_bg = Colors.BG.rgb(68,59,161)
    purple1_fg = Colors.FG.rgb(68,59,161)

    purple2_bg = Colors.BG.rgb(87, 87, 145)
    purple2_fg = Colors.FG.rgb(87, 87, 145)

    #status = 'Clear'
    #temp = 74
    #weather = purple2_fg+'\ue0b6'+Colors.reset+purple2_bg+Weather.sunny+' '+status+' '+Colors.reset+purple2_bg+purple1_fg+'\ue0b6'+Colors.reset+purple1_bg+' '+str(temp)+'°F '+Colors.reset
    #weather_length = 3+len(status)+3+len(str(temp))+3
    extra = os.get_terminal_size().columns - time_length
    print(time_bar+(' '*extra))

def stats_bar():
    red1_bg = Colors.BG.rgb(168, 32, 69)
    red1_fg = Colors.FG.rgb(168, 32, 69)

    red2_bg = Colors.BG.rgb(209, 79, 101)
    red2_fg = Colors.FG.rgb(209, 79, 101)

    storage_f = f'{"{:.2f}".format(storage)}'
    ram_f = f'{"{:.2f}".format(ram)}'
    bar = red1_bg+' STORAGE '+storage_f+'% '+Colors.reset+red1_fg+red2_bg+'\ue0b4'+Colors.reset+red2_bg+' RAM '+ram_f+'% '+Colors.reset+red2_fg+'\ue0b4'+Colors.reset
    bar_len = 9+len(storage_f)+8+len(ram_f)+3
    print(bar+' '*(os.get_terminal_size().columns-bar_len))

def statsloop():
    global storage, ram
    while True:
        storage = getstats.get_storage(ip)
        ram = getstats.get_ram(ip)
        time.sleep(1)


def services_1():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    green_fg = Colors.FG.rgb(61, 179, 112)
    print(grey_fg+'╭'+green_fg+'SERVICES'+grey_fg+'—'*(os.get_terminal_size().columns - 10)+'╮'+Colors.reset)

def services_2():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    green_fg = Colors.FG.rgb(61, 179, 112)
    yellow_fg = Colors.FG.rgb(245, 216, 103)
    s = grey_fg+'│'+Colors.reset
    w = int((os.get_terminal_size().columns - 2)/6)
    diff = (os.get_terminal_size().columns - 2) - 6*w
    s += ' '*int(diff/2)
    for service in services:
        if service in available:
            s += green_fg + (('{: ^'+str(w)+'}').format('\uf111 ' + service)) + Colors.reset
        else:
            s += yellow_fg + (('{: ^'+str(w)+'}').format('\uf071 ' + service)) + Colors.reset
    s += ' '*(diff-int(diff/2))+grey_fg+'│'+Colors.reset
    print(s)

def services_3():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    print(grey_fg + '╰' + '—' * (os.get_terminal_size().columns - 2) + '╯' + Colors.reset)

def pingall():
    while True:
        for service in services:
            if ping.ping(services[service][0],services[service][1]) and service not in available:
                available.append(service)
            elif not ping.ping(services[service][0],services[service][1]) and service in available:
                available.remove(service)
        time.sleep(5)

def deluge_1():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    blue_fg = Colors.FG.rgb(45, 87, 204)
    w1 = int(os.get_terminal_size().columns/2)
    w2 = os.get_terminal_size().columns - w1
    window1 = grey_fg+'╭'+blue_fg+'DOWNLOADS'+grey_fg+'―'*(w1 - 11)+'╮' + Colors.reset
    window2 = grey_fg+'╭'+blue_fg+'SEEDING'+grey_fg+'―'*(w2 - 9)+'╮' + Colors.reset
    print(window1+window2)

def deluge_2():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    blue_fg = Colors.FG.rgb(45, 87, 204)
    w1 = int(os.get_terminal_size().columns / 2)
    w2 = os.get_terminal_size().columns - w1
    for i in range(5):
        window1 = grey_fg+'│  '+blue_fg
        cw = 6
        if len(downloads) > i:
            window1 += '{:.2f}% '.format(downloads[i][1])
            cw += len('{:.2f}% '.format(downloads[i][1]))
            window1 += Colors.reset + downloads[i][0][:w1-cw] + ' '*(w1-len(downloads[i][0][:w1-cw])-cw) + grey_fg + '  │'+Colors.reset
        else:
            window1 += grey_fg+' '*(w1-4)+'│'+Colors.reset

        window2 = grey_fg+'│  '+Colors.reset
        if len(seeds) > i:
            window2 += Colors.reset + seeds[i][:w2 - 6] + ' '*(w2-len(seeds[i][:w2 - 6]) - 6) + grey_fg + '  │'+Colors.reset
        else:
            window2 += grey_fg+' '*(w2-4)+'│'+Colors.reset
        print(window1+window2)

def deluge_3():
    grey_fg = Colors.FG.rgb(64, 64, 64)
    w1 = int(os.get_terminal_size().columns / 2)
    w2 = os.get_terminal_size().columns - w1
    window1 = grey_fg + '╰' + '―' * (w1 - 2) + '╯' + Colors.reset
    window2 = grey_fg + '╰' + '―' * (w2 - 2) + '╯' + Colors.reset
    print(window1 + window2)

def gettorrents():
    global downloads, seeds
    while True:
        torrents = deluge.getTorrents(url, password)
        downloads = []
        seeds = []
        for torrent in torrents:
            if not torrents[torrent]['paused']:
                if torrents[torrent]['state'] == 'Downloading':
                    downloads.append((torrents[torrent]['name'],torrents[torrent]['progress']))
                elif torrents[torrent]['state'] == 'Seeding':
                    seeds.append(torrents[torrent]['name'])
        time.sleep(5)


def blank():
    print(' '*os.get_terminal_size().columns)


stats_thread = threading.Thread(target=statsloop)
stats_thread.start()
ping_thread = threading.Thread(target=pingall)
ping_thread.start()
torrent_thread = threading.Thread(target=gettorrents)
torrent_thread.start()

while True:
    print(Terminal.reset, end='')
    top_bar()
    stats_bar()
    blank()
    services_1()
    services_2()
    services_3()
    deluge_1()
    deluge_2()
    deluge_3()
    for i in range(os.get_terminal_size().lines-14):
        blank()
