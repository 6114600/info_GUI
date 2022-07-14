import json

import cv2
import psutil
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import random
# import radar
import datetime

import utils
from utils import room_num_format

def image_process():
    for k in ['111','110','101','011','100','010','001','000']:
        img = cv2.imread(f'images/{k}.png')
        img = cv2.resize(img,(len(img[0])//4,len(img)//4))
        for i in range(len(img)):
            for j in range(len(img[0])):
                if all(img[i,j,:]) == 0:
                    img[i,j,:] = [255,255,255]

        # img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        cv2.imwrite(f'images/{k}.png',img)

def _test_data():
    for name, data_name in zip(['c.xlsx','h.xlsx','l.xlsx'],['冷水表读数','热水表读数','电表读数']):
        print(f'-------------{data_name}-------------')
        writer = pd.ExcelWriter(name, mode='a', engine='openpyxl')
        for i in range(2,6):
            for j in range(1,15):
                print(f'Process {i}-{j}....',end='')
                df = pd.DataFrame()
                floor = str(i)
                room = room_num_format(i,j)
                data_ = [200]
                # Date = []
                for date in pd.date_range(start=datetime.datetime.strptime('20100101', '%Y%m%d'),end=datetime.datetime.strptime('20110101', '%Y%m%d'), freq='d'):
                    data_.append(data_[len(data_)-1] + random.randint(0,50))
                # df['楼层'] = [floor] * (+1)
                # df['房间号'] = [room] * (n+1)
                df['日期'] = pd.date_range(start=datetime.datetime.strptime('20100101', '%Y%m%d'),end=datetime.datetime.strptime('20110101', '%Y%m%d'), freq='d')
                df[data_name] = data_[:-1]
                df.to_excel(writer,sheet_name=room,index=False)
                writer.save()
                print('Done')
        writer.close()

def _test_data_2():
    df = pd.DataFrame(columns=['楼层','房间号','热水表状态','冷水表状态','电表状态'])
    for floor in range(2,11):
        for room in range(1,38):
            h_status = random.uniform(0,1) > 0.1
            c_status = random.uniform(0, 1) > 0.1
            e_status = random.uniform(0, 1) > 0.1
            df = df.append({'楼层':'%02d'%(floor),'房间号':'%02d%02d'%(floor,room),
                       '热水表状态':h_status,'冷水表状态':c_status,'电表状态':e_status},ignore_index=True)
    print(df)
    df.to_excel('status.xlsx',sheet_name='1')

def get_database():
    mydb = mysql.connector.connect(host='localhost',user='root',passwd='1448856147',database='water_electri',auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()

    for floor in range(2,11):
        for room in range(1,38):
            room_num = utils.room_num_format(floor,room)
            sql_text = "CREATE TABLE if not exists Room_{} (Squence int(10) auto_increment primary key," \
                       "date_time DATETIME DEFAULT NULL," \
                       "water_h FLOAT(4) DEFAULT NULL," \
                       "water_c FLOAT(4) DEFAULT NULL," \
                       "electri FLOAT(4) DEFAULT NULL)".format(room_num)
            # sql_text = 'drop table Room_{}'.format(room_num)
            print(sql_text)

            mycursor.execute(sql_text)
            # for x in mycursor:
            #     print(x)

def putintodatabase():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='1448856147', database='water_electri',
                                   auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()
    for floor in range(2,11):
        for room in range(1,38):
            room_num = utils.room_num_format(floor,room)
            values = [0, 0, 0]
            # for year in [2015,2018,2020]:
            #     for month in [2,7,12]:
            #         for day in [4,15,21]:
            #             for time in [8,9,10,11]:
            #                 date_time_str = "%d-%d-%d %02d:01:01"%(int(year),int(month),int(day),int(time))
            #                 for i in range(3):
            #                     values[i] += random.randint(500,1000)
            sql_text = f"INSERT INTO address_config (房间号) values('{room_num}')"
            mycursor.execute(sql_text)
    mydb.commit()
    # engine = create_engine('mysql+mysqlconnector:// root:1448856147@127.0.0.1/water_electri?auth_plugin=mysql_native_password')
    # df = pd.read_excel('h.xlsx',sheet_name='0201')

    # print(df.head(5))
    # df.to_sql('0201',engine,index=False,if_exists='append')

if __name__ == '__main__':
    # _test_data_2()
    # image_process()
    # get_database()
    # with open('config/config.json','r') as f:
    #     c = json.load(f)
    #     print(c)
    # putintodatabase()

    # df = pd.read_excel('h.xlsx','0201')
    # df = df.sort_index(ascending=False).head(1)
    # print(df)

    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name().startswith('backGround'):
            print(p.name())