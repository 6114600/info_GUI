import cv2
import pandas as pd
import numpy as np
import random
import radar
import datetime
from utils import room_num_format

def image_process():
    img = cv2.imread('images/lightening.png')
    img = cv2.resize(img,(34,50))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if all(img[i,j,:]) == 0:
                img[i,j,:] = [255,255,255]
    cv2.imwrite('images/lightening.png',img)

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
if __name__ == '__main__':
    _test_data()
    # print(pd.date_range(start=datetime.datetime.strptime('20000101', '%Y%m%d'),end=datetime.datetime.strptime('20100101', '%Y%m%d'), freq='d'))