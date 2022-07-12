from concurrent.futures import ThreadPoolExecutor # IO密集型，应用python多线程。无需多进程
import socket
import time
from unittest import result
import sys
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# from utils.SQLReadWriteSpecificRoom import SQLreadRoom,SQLWriteRoom

# waterMeterAddr = bytes([0x01,0x03,0x00,0x00,0x00,0x02,0xc4,0x0b])
# waterRecvDataBuffer = bytes()

# elecMeterReadAddr = bytes([0xFE,0xFE,0xFE,0xFE,0x68,0x52,0x00,0x26,0x05,0x22,0x00,0x68,0x11,0x04,0x33,0x33,0x33,0x33,0x50,0x16])
# elecRecvDataBuffer = bytes()

elecControllerIPlist = ['198.198.198.20','198.198.198.21','198.198.198.22','198.198.198.23','198.198.198.24',
                        '198.198.198.25','198.198.198.26','198.198.198.27','198.198.198.28']
elecAddressList      = ['1','2']

waterControllerIPlist = ['198.198.198.1','198.198.198.2','198.198.198.3','198.198.198.4','198.198.198.5','198.198.198.6',
                         '198.198.198.7','198.198.198.8','198.198.198.9','198.198.198.10','198.198.198.111','198.198.198.12',
                         '198.198.198.13','198.198.198.14','198.198.198.15','198.198.198.16','198.198.198.17','198.198.198.18',
                         '198.198.198.19']
wawaterAddressList   = [f'{i}' for i in range(1,37)]

#######################电表
#读一个HF5122控制器，一次读取所有其所控制的电表。创建9个线程，即可得到所有数据
def TCPIPReadEleMeter2SQL(IpAddress:str): 
    elecMeterReadAddr = bytes([0xFE,0xFE,0xFE,0xFE,0x68,0x52,0x00,0x26,0x05,0x22,0x00,0x68,0x11,0x04,0x33,0x33,0x33,0x33,0x50,0x16])
    socket.setdefaulttimeout(20)#设置超时时间为,单位秒
    mySocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for elecAddress in elecAddressList:
        try:
            mySocketTCP.connect((IpAddress, 8899))# IP是参数，但是端口号一定是8899.
            time.sleep(0.001) # 0.001 秒，用于挂起线程，使python切换到其他线程。取决于tcp连接函数是否会自动阻塞
        except socket.error:
            #tcp连接控制器失败，向SQL写入错误码：HF5122连接失败
            room = getRoomByAddress(IpAddress, elecAddress)
            writeElecData2SQL(room,-1)#错误码,tcp连接出错
            print("TCPIP连接失败")
            return

        else: #若创建tcp连接成功，则继续执行代码
            mySocketTCP.send(elecMeterReadAddr) # 发送读取电表数据的字节序列
            try:
                receivedBytes = mySocketTCP.recv(24) # 等待接收电表传回来的数据，阻塞。
                readTimes = 1
                while(elecDataCheck(receivedBytes) == 0): #进行校验，若校验数据对不上，再次读取
                    mySocketTCP.send(elecMeterReadAddr)
                    receivedBytes = mySocketTCP.recv(24)
                    readTimes += 1
                    if (readTimes > 3):  #读取次数超过3次
                        break
                
                if(readTimes <= 3): #读取次数不超过3次，则写入
                    receivedData = convertElecBytes(receivedBytes) #转换数据
                    room = getRoomByAddress(IpAddress,elecAddress)#根据IP地址和电表地址从数据库中获取房间号
                    writeElecData2SQL(room,receivedData)  #写入数据库

                else:#3次数据校验不通过，写入错误码
                    room = getRoomByAddress(IpAddress,elecAddress)
                    writeElecData2SQL(room,-2)#接收到了设备的数据，但校验不通过

                mySocketTCP.close()
            except socket.timeout:
                room = getRoomByAddress(IpAddress,elecAddress)
                writeElecData2SQL(room,-3) #电表无数据返回
                mySocketTCP.close()
                
            return

def elecDataCheck(byte2check:bytes):#  将除了最后两个数据的所有数据相加，取低字节，与倒数第二个字节比较
    result_ = 0
    for byte in byte2check[0:-2]:
        # print(byte)
        result_ += byte
    # return result_%256

    if result_ % 256 == byte2check[-2]:
        return 1  #校验成功
    return 0 #校验失败

def convertElecBytes(bytes2convert):
    totalElec = 0
    for i in range(0,4):#共读取4个数字
        BCDtemp = bytes2convert[17 - i] - 51
        temp    = (BCDtemp >> 4) * 10 + (BCDtemp & 0x0f)
        totalElec = totalElec * 100 + temp
        print('%#x'%(bytes2convert[17 - i] - 51)) # 51 是33H
    return totalElec / 100

def getRoomByAddress(IpAddress, elecAddress):
    room = '0201'
    return room

def writeElecData2SQL(room,data):
    pass

#################################水表
#读一个HF5122控制器，一次读取所有其所控制的水表。创建9个线程，即可得到所有水表数据
def TCPIPReadWaterMeter2SQL(IpAddress:str): 
    waterMeterReadAddr = bytes([0x01,0x03,0x00,0x00,0x00,0x02,0xc4,0x0b])
    socket.setdefaulttimeout(20)#设置超时时间 秒
    mySocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for waterAddress in wawaterAddressList:
        try:
            mySocketTCP.connect((IpAddress, 8899))# IP是参数，但是端口号一定是8899.
            time.sleep(0.001) # 0.001 秒，用于挂起线程，使python切换到其他线程。取决于tcp连接函数是否会自动阻塞
        except socket.error:
            #tcp连接控制器失败，向SQL写入错误码：HF5122连接失败
            room, isHot = getWaterRoomByAddress(IpAddress,waterAddress)#根据IP地址和电表地址从数据库中获取房间号
            #isHot表示是否是热水表
            writeWaterData2SQL(room, isHot, -1)#错误码,tcp连接出错
            print("TCPIP连接失败")
            return

        else: #若创建tcp连接成功，则继续执行代码
            mySocketTCP.send(waterMeterReadAddr) # 发送读取水表数据的字节序列
            try:
                receivedBytes = mySocketTCP.recv(24) # 等待接收电表传回来的数据，阻塞。
                readTimes = 1
                while(waterDataCheck(receivedBytes) == 0): #进行校验，若校验数据对不上，再次读取
                    mySocketTCP.send(waterMeterReadAddr)
                    receivedBytes = mySocketTCP.recv(24)
                    readTimes += 1
                    if (readTimes > 3):  #读取次数超过3次
                        break
                
                if(readTimes <= 3): #读取次数不超过3次，则写入
                    receivedData = convertWaterBytes(receivedBytes) #转换数据
                    room,isHot = getWaterRoomByAddress(IpAddress,waterMeterReadAddr)
                    writeWaterData2SQL(room,isHot,receivedData)  #x写入数据库

                else:#3次数据校验不通过，写入错误码
                    room, isHot = getWaterRoomByAddress(IpAddress,waterAddress)#根据IP地址和电表地址从数据库中获取房间号
                #isHot表示是否是热水表
                    writeWaterData2SQL(room, isHot, -2)#接收到设备的数据，但是数据校验错误
                mySocketTCP.close()
            except socket.timeout:
                room, isHot = getWaterRoomByAddress(IpAddress,waterAddress)#根据IP地址和电表地址从数据库中获取房间号
                #isHot表示是否是热水表
                writeWaterData2SQL(room, isHot, -3)#水表无数据返回，线缆断开或水表损坏
                mySocketTCP.close()

            return

def waterDataCheck(byte2check:bytes):#  crc16 moudbus
    crc16 = 0xffff
    poly  = 0xa001
    for byte in byte2check[0:-2]:
        crc16 = byte ^ crc16
        for i in range(8):
            if 1 & (crc16) == 1:
                crc16 = crc16 >> 1
                crc16 = crc16 ^ poly
            else:
                crc16 = crc16 >> 1
    # print("crc16:%#x"%crc16)
    # print("crc16高位：%#x"%((crc16>>8)&0xff))
    # print("crc16低位：%#x"%(crc16&0xff))
    if ((crc16>>8)&0xff == byte2check[-1]) and ((crc16&0xff) == byte2check[-2]):
        return 1 # 校验成功
    return 0  #校验失败

def convertWaterBytes(bytes2convert):
    totalWater = 0
    for i in range(3,7):#共读取4个字节数据
        totalWater = totalWater * 256 + (bytes2convert[i])
        # print(bytes2convert[i])
    return totalWater / 100

def getWaterRoomByAddress(IpAddress, waterAddress):
    room = '0201'
    isHot = 1

    return room,isHot

def writeWaterData2SQL(room, isHot, data):
    pass

if __name__ == "__main__":
    # #这是一次接收到的电表数据
    # elecRecvedData = bytes([0x68,0x52,0x00,0x26,0x05,0x22,0x00,0x68,0x91,0x08,0x33,0x33,0x33,0x33,0x3a,0x33,0x33,0x33,0xa7,0x16])
    #这是电表发送123456.78kWh的数据 
    # elecRecvedData = bytes([0x68,0x52,0x00,0x26,0x05,0x22,0x00,0x68,0x91,0x08,0x33,0x33,0x33,0x33,0xab,0x89,0x67,0x45,0x,0x16])
    # print(elecDataCheck(elecMeterReadAddr))
    # print(convertElecBytes(elecRecvedData))
    # print('end')
    # print(wawaterAddressList)

    # waterReceddData = bytes([0x01,0x03,0x04,0x00,0x00,0x00,0xc8,0xfb,0xa5])#这是一次水表接收到的数据实例，表显2吨
    # # print(convertWaterBytes(waterReceddData))
    # print(waterDataCheck(waterReceddData))
    # print(convertWaterBytes(waterReceddData))
