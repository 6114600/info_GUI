import time
from utils.time import ntpClient
from utils.loghelper import set_logger
import schedule
import threading

logger = set_logger('info','log/test.log')

def job():
    ntpClient()

def run_threaded(job_function):
    job_thread = threading.Thread(target=job_function)
    job_thread.start()
    print('开始校时')
    logger.info('开始校时')

schedule.every(10).seconds.do(run_threaded,job)

while True:
    schedule.run_pending()
    time.sleep(1)
