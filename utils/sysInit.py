#用于读取excel表格中各房间，各表的地址，

import json
from mimetypes import init
import os
import datetime
import mysql.connector as sqlCon
import sys
import io

from regex import F
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def meterDataBaseInit(addressMySQL:dict):
    connection = sqlCon.connect(host = addressMySQL['mySQL_host'],
                                port = addressMySQL['mySQL_port'],
                                user = addressMySQL['mySQL_user'],
                                password = addressMySQL['mySQL_password']
                            )



    cursor = connection.cursor()

    # 查询数据库是否存在，不存在则创建数据库
    cursor.execute("create database if not exists `1elec_meter`;") #电表数据库
    cursor.execute("create database if not exists `2hot_water_meter`;") #热水数据库
    cursor.execute("create database if not exists `3cold_water_meter`;") #冷水数据库


    #在数据库中给每个房间创建一个表格 三个字段 {日期 时间 当前表显} {date time currentVal}
    cursor.execute("use `1elec_meter`;")

    for i in range(2,11): #2楼到10楼，暂时写3做测试  注意range(2,4) = [2 3]
        for j in range(1,38): #1号房间到37号，暂时写到2
            # 表格不存在则创建表格
            cursor.execute("create table if not exists `room%02d%02d`\
                            (`date_time` datetime, \
                            `current_val` decimal(10,2));"%(i, j))


    cursor.execute("use `2hot_water_meter`;")

    for i in range(2,4): #2楼到10楼，暂时写3做测试  注意range(2,4) = [2 3]
        for j in range(1,3): #1号房间到37号，暂时写到2
            # 表格不存在则创建表格
            cursor.execute("create table if not exists `room%02d%02d`\
                            (`date_time` datetime, \
                            `current_val` decimal(10,2));"%(i, j))

    cursor.execute("use `3cold_water_meter`;")

    for i in range(2,4): #2楼到10楼，暂时写3做测试  注意range(2,4) = [2 3]
        for j in range(1,3): #1号房间到37号，暂时写到2
            # 表格不存在则创建表格
            cursor.execute("create table if not exists `room%02d%02d`\
                            (`date_time` datetime, \
                            `current_val` decimal(10,2));"%(i, j))

    cursor.close()
    connection.commit()
    connection.close()

def addressOfMeterDataBaseInit():
    pass

def sysInit(initManually = False): #初始化有两种情况，一种是手动初始化，一种是第一次运行程序初始化
    #初次启动时，查看log文件夹内是否含有文件initLog.log，若有，且initMannually为False，则不是初次启动，直接退出
    if not os.path.exists("./log/initLog.log") or initManually:
        print("第一次运行或配置被修改，正在初始化")
        jsonF = open('./config/config.json','r')
        jsonDict = json.load(jsonF)
        jsonF.close()

        meterDataBaseInit(jsonDict)

        timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        initLog = open("./log/initLog.log",'a')
        initLog.write(timeNow + "\tsystem initialized, mySQL database created.\n")
        initLog.close()
        print("初始化结束")
        return

        
    #没有该文件，说明程序第一次启动，则创建数据库，在数据库中创建表格
    else:
        print("程序不是第一次运行，不需要初始化")
        return
        


if __name__ == "__main__":
    sysInit(initManually= True)

        

