

import mysql.connector as sqlCon
from sklearn import datasets

#@room: class 'str', 'room0201','room1025' etc.
#@dateStart: class 'str', '2022-06-29' etc.
#@dateEnd: class 'str', '2022-06-29' etc.
def SQLreadRoom(room, dateTimeStart, dateTimeEnd):
    connection = sqlCon.connect(host = 'localhost',
                                port = '3306',
                                user = 'root',
                                password = '1461',
                                database = '1elec_meter') #电表

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `%s`\
                    WHERE \
                    `date_time` >= '%s' AND `date_time` <= '%s';"
                    %(room,dateTimeStart,dateTimeEnd))

    elecMeterData = cursor.fetchall()
    # print("elecMeterData:",elecMeterData)
    cursor.close()
    connection.close()

    connection = sqlCon.connect(host = 'localhost',
                            port = '3306',
                            user = 'root',
                            password = '1461',
                            database = '2hot_water_meter') #电表

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `%s`\
                    WHERE \
                    `date_time` >= '%s' AND `date_time` <= '%s';"
                    %(room,dateTimeStart,dateTimeEnd))

    hotWaterMeterData = cursor.fetchall()
    cursor.close()
    connection.close()

    connection = sqlCon.connect(host = 'localhost',
                            port = '3306',
                            user = 'root',
                            password = '1461',
                            database = '3cold_water_meter') #电表

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `%s`\
                    WHERE \
                    `date_time` >= '%s' AND `date_time` <= '%s';"
                    %(room,dateTimeStart,dateTimeEnd))

    coldWaterMeterData = cursor.fetchall()
    cursor.close()
    connection.close()

    returnData = []
    for r in elecMeterData:
        returnData.append(r)

    return elecMeterData, hotWaterMeterData, coldWaterMeterData
                    

#@dataType: class 'str', '1elec_meter', '2hot_water_meter', '3cold_water_meter'
#@room: class 'str', 'room0201','room1025' etc.
#@date: class 'str', '2022-06-29' etc.
#@time: class 'str', '22:05:35' etc.
#@currentVal: Decimal, 102.25   etc.
def SQLWriteRoom(dataBase: str, room: str, dateTime: str, currentVal):
    connection = sqlCon.connect(host = 'localhost',
                                port = '3306',
                                user = 'root',
                                password = '1461',
                                database = dataBase) #电表,热水还是冷水

    cursor = connection.cursor()

    cursor.execute("create table if not exists `%s`\
                         (`date_time` datetime, \
                         `current_val` decimal(10,2));"%(room))

    cursor.execute("INSERT INTO `%s` \
                    VALUES('%s',%f);"\
                        %(room, dateTime, currentVal))

    cursor.close()
    connection.commit()#对数据库进行修改时  需要此句
    connection.close()


# if __name__ == '__main__':
