import pandas as pd
import glob
from datetime import datetime  #タイムスタンプに使用するライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ

timestamp = datetime.today()
filename = timestamp.strftime("%Y%m%d%H%M%S")

# パスで指定したファイルの一覧をリスト形式で取得. 
csv_files = glob.glob("/home/pi/Documents/adxl355/adxl355_data/*.csv")

#読み込むファイルのリストを表示
for a in natsorted(csv_files):
    #print(a)
#csvファイルの中身を追加していくリストを用意
data_list = []
#読み込むファイルのリストを走査
for file in natsorted(csv_files):
    data_list.append(pd.read_csv(file))

#リストを全て行方向に結合
#axis=0:行方向に結合, sort
df = pd.concat(data_list, axis=0, sort=True)
df.to_csv("/home/pi/Documents/adxl355/adxl355_data/"+filename+"_total"".csv",index=False)