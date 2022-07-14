import traceback
import pandas as pd
from sqlalchemy.engine import create_engine

def get_data(room_num,constrains):
    con = create_engine('mysql+mysqlconnector:// root:1448856147@127.0.0.1/water_electri?auth_plugin=mysql_native_password')
    df = None
    try:
        if constrains is None:
            sql_text = f'select * from room_{room_num} order by date_time desc limit 0,50'
        else:
            sql_text = f"select Squence, date_time, {constrains[2]} from room_{room_num} where date_time between '{constrains[0]}' and '{constrains[1]}' order by date_time desc"
        df = pd.read_sql_query(sql_text, con=con)
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        con.dispose()
    return df


def get_login_info(user):
    con = create_engine(
        'mysql+mysqlconnector:// root:1448856147@127.0.0.1/water_electri?auth_plugin=mysql_native_password')
    if user is None:
        sql_text = f"SELECT * from users_info"
    else:
        sql_text = f"SELECT * from users_info where user='{user}'"
    df = pd.read_sql_query(sql_text, con=con)
    con.dispose()
    return df


def get_address(num):
    con = create_engine(
        'mysql+mysqlconnector:// root:1448856147@127.0.0.1/water_electri?auth_plugin=mysql_native_password')
    if num is None:
        sql_text = f"SELECT * from address_config"
    else:
        sql_text = f"SELECT * from address_config where room_num='{num}'"
    df = pd.read_sql_query(sql_text, con=con)
    con.dispose()
    return df


def edit_database(sql_text):
    con = create_engine(
        'mysql+mysqlconnector:// root:1448856147@127.0.0.1/water_electri?auth_plugin=mysql_native_password')
    con.execute(sql_text)
    con.dispose()


def get_status(room_num):
    df_status = pd.read_excel('D:\资料\研究生\info_GUI\status.xlsx', sheet_name='1')
    status = df_status[df_status['房间号']==int(room_num)][['热水表状态','冷水表状态','电表状态']]
    status = status.reset_index(drop=True)
    # print(status,type(status))
    return status


if __name__ == '__main__':
    get_data('0201')
