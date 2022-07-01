import cv2
import pandas as pd
import numpy as np
import random
# import radar
import datetime
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


if __name__ == '__main__':
    # _test_data_2()
    image_process()
    # print(pd.date_range(start=datetime.datetime.strptime('20000101', '%Y%m%d'),end=datetime.datetime.strptime('20100101', '%Y%m%d'), freq='d'))