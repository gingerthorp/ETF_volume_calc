import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform


# 운용체제 환경에 따라 글꼴 선택.
osSelect = platform.system()
if osSelect == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
elif osSelect == 'Darwin':
    rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("1min_ETF.db", isolation_level=None)
    # 커서 획득
    c = conn.cursor()

    stock_info = {
        "A122630": {
            "stock_code": "A122630",
            "stock_name": "KODEX_레버리지"
        },
        "A252670": {
            "stock_code": "A252670",
            "stock_name": "KODEX_200선물인버스2X"
        },
        "A233740": {
            "stock_code": "A233740",
            "stock_name": "KODEX_코스닥150_레버리지"
        },
        "A251340": {
            "stock_code": "A251340",
            "stock_name": "KODEX_코스닥150선물인버스"
        }
    }

    race_result = None

    for key in stock_info.keys():

        query = c.execute(f"SELECT '[' || substr(date,9,4) || ']' as mins, AVG(close*volume) as {stock_info[key]['stock_name']} "
                          f"FROM {stock_info[key]['stock_code']} "
                          #f"WHERE (date) > 202101010000 "
                          f"GROUP BY mins")

        cols = [column[0] for column in query.description]

        if race_result is None:
            race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols, index="mins")
        else:
            result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols, index="mins")
            race_result = pd.concat([race_result, result], axis=1)

    idx_nm_1 = [f"[{i}]" for i in range(1521, 1530, 1)]
    idx_nm_1 += [f"[{i}]" for i in range(1531, 1560, 1)]
    idx_nm_1 += [f"[{i}]" for i in range(1600, 1621, 1)]
    idx_nm_1 += ["[1630]"]
    print(idx_nm_1)
    race_result = race_result.drop(idx_nm_1)

    race_result = race_result / 100000000   # 1억 단위.
    print(race_result.to_string())

    plt.rcParams["figure.figsize"] = (14, 4)
    race_result.plot(title="2019년 이후 분봉당 평균 거래대금(억 원)")
    plt.grid(True)
    plt.xticks(rotation=90)


    plt.show()



