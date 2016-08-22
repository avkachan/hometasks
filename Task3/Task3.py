import psutil
import schedule
import datetime
import json
import configparser

snapshot = 0
config = configparser.ConfigParser()
config.read('config.ini')
type = config.get('setup', 'type')
time_1 = config.get('setup', 'time_m')
cleartxt = open('infa.txt', "w")
cleartxt.close()
clearjson = open("infa.json", "w")
clearjson.close()
def txt ():
    global snapshot
    snapshot += 1
    f = open('infa.txt', "a")
    format = '%Y-%m-%d %H:%M:%S %Z'
    time_now = datetime.datetime.now()
    time_stmp = datetime.datetime.strftime(time_now, format)
    f.write('Snapshot {0}:\ntime - {1}\n'.format(snapshot, time_stmp))
    f.write('Overall CPU load: {} %\n'.format(psutil.cpu_percent()))
    f.write('Overall memory usage: {} MB\n'.format((psutil.virtual_memory()[3]/1024/1024).__round__(2)))
    f.write('HDD read: {} MB\n'.format((psutil.disk_io_counters()[2]/1024/1024).__round__(2)))
    f.write('HDD write: {} MB\n'.format((psutil.disk_io_counters()[3]/1024/1024).__round__(2)))
    f.write('Network sent: {} MB\n'.format((psutil.net_io_counters()[0]/1024/1024).__round__(2)))
    f.write('Network recieve: {} MB\n'.format((psutil.net_io_counters()[1]/1024/1024).__round__(2)))
    f.write("\n")
    f.close()

def jsonf():
    global snapshot
    snapshot += 1
    format = '%Y-%m-%d %H:%M:%S %Z'
    time_now = datetime.datetime.now()
    time_stmp = datetime.datetime.strftime(time_now, format)
    top = {
        'Overall CPU load': str(psutil.cpu_percent()) + ' %',
        'Overall memory usage': str((psutil.virtual_memory()[3]/1024/1024).__round__(2)) + " MB",
        'HDD read': str((psutil.disk_io_counters()[2]/1024/1024).__round__(2)) + " MB",
        'HDD write': str((psutil.disk_io_counters()[3]/1024/1024).__round__(2)) + " MB",
        'Network sent': str((psutil.net_io_counters()[0]/1024/1024).__round__(2)) + " MB",
        'Network recieve': str((psutil.net_io_counters()[1] / 1024 / 1024).__round__(2)) + " MB"
    }
    data = ['SNAPSHOT ' +  str(snapshot) + ": " + str(time_stmp) + ": ", top]
    with open("infa.json", "a") as f:
        json.dump(data, f, indent=3, sort_keys=True)

if type == "txt":
    schedule.every(int(time_1)).seconds.do(txt)
elif type == "json":
    schedule.every(int(time_1)).seconds.do(jsonf)
while True:
    schedule.run_pending()
