import pandas as pd


def get_data(room_num):
    sheet = str(room_num)
    df_l = pd.read_excel('l.xlsx',sheet_name=sheet,index=False)
    df_c = pd.read_excel('c.xlsx', sheet_name=sheet, index=False)
    df_h = pd.read_excel('h.xlsx', sheet_name=sheet, index=False)
    df_b = pd.read_excel('b.xlsx', sheet_name=sheet, index=False)
    df_0 = pd.merge(df_h,df_c,on='日期')
    df_1 = pd.merge(df_b,df_l,on='日期')
    df = pd.merge(df_0,df_1)
    #TODO: mysql -> pd.dataframe
    return df

def get_data_by_room(path,room_num):
    df = pd.read_excel(path,sheet_name=str(room_num),index=False)
    return df


if __name__ == '__main__':
    df = get_data(101)
    print(df)