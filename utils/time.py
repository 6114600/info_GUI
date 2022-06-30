import ntplib
import os
import datetime
import time
import sys
sys.path.append(r".")
from utils.loghelper import set_logger

def ntpClient():
    hosts = ['0.cn.pool.ntp.org', '1.cn.pool.ntp.org', '2.cn.pool.ntp.org', '3.cn.pool.ntp.org']
    t = ntplib.NTPClient()
    logger = set_logger('info','./log/test.log')
    for host in hosts:
        try:
            r = t.request(host, port='ntp', version=4, timeout=5)
            if r:
                t = r.tx_time
                _date, _time = str(datetime.datetime.fromtimestamp(t))[:22].split(' ')
                os.system('date {} && time {}'.format(_date, _time))
                # print('\r',time.strftime('%Y-%m-%d %H:%M:%S'),'时间校准成功',end='')
                logger.info('已成功校时')
                return _date, _time
        except Exception as e:
            pass

if __name__ == '__main__':
    ntpClient()
