import psutil
import schedule
import datetime
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
type_1 = config.get('setup', 'type')
time_1 = config.get('setup', 'time_m')
cleartxt = open('infa.txt', "w")
cleartxt.close()
clearjson = open("infa.json", "w")
clearjson.close()
clearlog = open("log.log", "w")
clearlog.close()
dec_enabled = config.getboolean('setup', 'dec_enabled')


class Var:
    snapshot = 1

    def __init__(self):
        self.cpu = psutil.cpu_percent()
        self.mem = (psutil.virtual_memory()[3] / 1024 / 1024).__round__(2)
        self.hddr = (psutil.disk_io_counters()[2] / 1024 / 1024).__round__(2)
        self.hddw = (psutil.disk_io_counters()[3] / 1024 / 1024).__round__(2)
        self.nets = (psutil.net_io_counters()[0] / 1024 / 1024).__round__(2)
        self.netr = (psutil.net_io_counters()[1] / 1024 / 1024).__round__(2)
        self.fdata = '%Y-%m-%d %H:%M:%S %Z'
        self.time_now = datetime.datetime.now()
        self.time_stmp = datetime.datetime.strftime(self.time_now, self.fdata)

    def dec(log):
        def inner(*args, **kwargs):
            l = open('log.log', "a")
            l.write('Start\nSnapshot:{}\n'.format(Var.snapshot))
            l.write('Function name:{0},{1},{2}\n'.format(log.__name__, args, kwargs))
            log(*args, **kwargs)
            l.write('Stop\n')
            l.write('\n')
            l.close()
        return inner if dec_enabled else log


class Main(Var):
    @Var.dec
    def txt(self):
        Var.snapshot += 1
        f = open('infa.txt', "a")
        f.write('Snapshot {0}:\ntime - {1}\n'.format(self.snapshot, self.time_stmp))
        f.write('Overall CPU load: {} %\n'.format(self.cpu))
        f.write('Overall memory usage: {} MB\n'.format(self.mem))
        f.write('HDD read: {} MB\n'.format(self.hddr))
        f.write('HDD write: {} MB\n'.format(self.hddw))
        f.write('Network sent: {} MB\n'.format(self.nets))
        f.write('Network recieve: {} MB\n'.format(self.netr))
        f.write("\n")
        f.close()

    @Var.dec
    def jsonf(self):
        Var.snapshot += 1
        top = {
            'Overall CPU load': str(self.cpu) + ' %',
            'Overall memory usage': str(self.mem) + " MB",
            'HDD read': str(self.hddr) + " MB",
            'HDD write': str(self.hddw) + " MB",
            'Network sent': str(self.nets) + " MB",
            'Network recieve': str(self.netr) + " MB"
        }
        data = ['SNAPSHOT ' + str(self.snapshot) + ": " + str(self.time_stmp) + ": ", top]
        with open("infa.json", "a") as f:
            json.dump(data, f, indent=3, sort_keys=True)
            f.close()


@Var.dec
def run():
    if type_1 == "txt":
        x = Main()
        x.txt()
    elif type_1 == "json":
        x = Main()
        x.jsonf()
schedule.every(int(time_1)).seconds.do(run)
while True:
    schedule.run_pending()
