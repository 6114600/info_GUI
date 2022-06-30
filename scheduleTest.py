import time
from utils.loghelper import set_logger
import schedule
import threading
import json

def main_task():
    print(time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime()),end='')
    print('执行任务')

# TODO：开机自启动
class period_task(object):
    def __init__(self, main_task):
        self.logger = set_logger('info','log/test.log')
        fp = open('config/config.json', 'r')
        self.now_config = json.load(fp)
        self.main_task = main_task

    def start_main(self):
        # 解码配置周期 #TODO: 完整版
        period_str = self.now_config['cb_period']
        sec_period = int(period_str[-2:])
        schedule.every(sec_period).seconds.do(self.run_threaded, self.main_task).tag('main')
        self.logger.info('主要任务线程启动/重启')

    def start_config_detect(self):
        self.logger.info('配置监视线程启动')
        schedule.every(60).seconds.do(self.run_threaded, self.detect_config_change).tag('config_dectect')

    def detect_config_change(self):
        print(time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime()), end='')
        print('读取config')
        with open('config/config.json','r') as fp:
            config = json.load(fp)
        if not config['dscb']:
            schedule.clear('main')
        else:
            if config['cb_period'] == self.now_config['cb_period']:
                self.now_config = config
            else:
                self.now_config = config
                schedule.clear('main')
                self.start_main()
        print(config)

    def run_threaded(self,job_function):
        job_thread = threading.Thread(target=job_function)
        job_thread.start()

    def start_all(self):
        self.start_main()
        self.start_config_detect()
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    task = period_task(main_task)
    task.start_all()