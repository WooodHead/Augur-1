import logging

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='sched.log',level=logging.INFO)

from db.DB import DB
import schedule
import threading
import time

kline_types = {
    # type: interval (min)
    3: 15,
    5: 60
}        

threads = set()

def update_all_klines(kline_type):
    db = DB()
    try:
        db.update_all_klines(kline_type)
    except Exception as err:
        print(err)
    threads.remove('update_all_klines-%s' % kline_type)

def update_all_symbols():
    db = DB()
    try:
        db.update_all_symbols()
    except Exception as err:
        print(err)
    threads.remove('update_all_symbols')

def update_all_coins():
    db = DB()
    try:
        db.update_all_coins()
    except Exception as err:
        print(err)
    threads.remove('update_all_coins')    

def run_threaded(job, *args):
    name = [job.__name__]
    name.extend(args)
    name = [str(n) for n in name]
    job_name = '-'.join(name)
    if job_name not in threads:
        threads.add(job_name)
        job_thread = threading.Thread(target=job, name=job_name, args=args)
        job_thread.start()
    else:
        print('%s already running' % job_name)

for t in kline_types:
    schedule.every(kline_types[t]).minutes.do(run_threaded, update_all_klines, t)

schedule.every(1).days.do(run_threaded, update_all_symbols)
schedule.every(1).days.do(run_threaded, update_all_coins)

while True:
    schedule.run_pending()
    time.sleep(60)