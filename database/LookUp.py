import random
import time

import mysql.connector
import threading
import json
import datetime
import pandas as pd
from sqlalchemy.engine import create_engine
from utils.loghelper import set_logger
from utils import room_num_format

logger = set_logger('debug','./log/test.log')

def ReadElectriMeters():
    # TODO: 读取电表
    # 产生测试数据
    df = pd.DataFrame(columns=['room', 'e_value'])

    index = 0
    for floor in range(2, 11):
        for room in range(1, 38):
            # temp_df = pd.read_excel('../h.xlsx',room_num_format(floor,room)).sort_index(ascending=False).head(1)
            value = random.randint(50, 100)
            # temp_df = pd.read_excel('../c.xlsx',room_num_format(floor,room)).sort_index(ascending=False).head(1)
            df.loc[index] = [room_num_format(floor, room), value]
            index += 1

    return df

def ReadWaterMeters():
    # TODO: 读取水表
    # 产生测试数据
    df = pd.DataFrame(columns=['room','hw_value','cw_value'])

    index = 0
    for floor in range(2,11):
        for room in range(1,38):
            # temp_df = pd.read_excel('../h.xlsx',room_num_format(floor,room)).sort_index(ascending=False).head(1)
            hw_value = random.randint(50,100)
            # temp_df = pd.read_excel('../c.xlsx',room_num_format(floor,room)).sort_index(ascending=False).head(1)
            cw_value = random.randint(50,100)
            df.loc[index] = [room_num_format(floor,room),hw_value,cw_value]
            index += 1

    return df

class LookUp_Helper(object):
    def __init__(self):
        self.db_cursor = None
        # 读取配置文件，获得数据库连接参数
        with open('./config/config.json','r') as f:
            self.config = json.load(f)

        # 初始化数据库连接
        self.database_check()

    def database_check(self):
        try:
            self.db_connect = mysql.connector.connect(host=self.config['db_host'],user=self.config['db_user'],
                                                 passwd=self.config['db_passwd'],database=self.config['db_name'],
                                                 auth_plugin=self.config['db_auth_plugin'])
            self.db_cursor = self.db_connect.cursor()
            print('成功与数据库连接')
            self.db_cursor.close()
            self.db_connect.close()
        except Exception as e:
            print(e)

    def database_connect(self):
        try:
            self.db_connect = mysql.connector.connect(host=self.config['db_host'],user=self.config['db_user'],
                                                 passwd=self.config['db_passwd'],database=self.config['db_name'],
                                                 auth_plugin=self.config['db_auth_plugin'])
            self.db_cursor = self.db_connect.cursor()
        except Exception as e:
            print(e)

    def database_close(self):
        self.db_connect = self.db_connect.close()

    def LookUpOnce(self):
        # 读取三表数据
        self.database_connect()
        timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{timeNow}\t已读取水表数据')
        logger.info(f'{timeNow}\t已读取水表数据')
        df_waters = ReadWaterMeters()
        time_ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{timeNow}\t已读取电表数据')
        logger.info(f'{time_}\t已读取电表数据')
        df_e = ReadElectriMeters()

        for floor in range(2, 11):
            for room in range(1, 38):
                room_num = room_num_format(floor,room)
                sql_text = f"Insert into room_{room_num} (date_time, water_h, water_c, electri) values('{timeNow}','{df_waters[df_waters['room']==room_num]['hw_value'].values[0]}'," \
                           f"'{df_waters[df_waters['room']==room_num]['cw_value'].values[0]}','{df_e[df_e['room']==room_num]['e_value'].values[0]}')"
                self.db_cursor.execute(sql_text)
                print(f'{room_num}已写入')
                time.sleep(0.05)

        self.db_connect.commit()
        self.database_close()

    def StartLookUp(self):
        self.lookup_thread = threading.Thread(target=self.LookUpOnce,)
        self.lookup_thread.setName('LookUpMeter')
        self.lookup_thread.start()


if __name__ == '__main__':
    lh = LookUp_Helper()
    lh.LookUpOnce()