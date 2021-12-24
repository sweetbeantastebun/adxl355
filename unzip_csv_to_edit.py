#coding:utf-8
"""
ファイル解凍
複数csvファイルを１つのファイルにまとめ出力する
"""
import zipfile
import paramiko
from datetime import datetime  #タイムスタンプを実行するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ（自然順アルゴリズム）
import pandas as pd
import schedule


def EDIT():
    """解凍"""
    #パス先
    path = "/home/pi/Documents/adxl355/adxl355_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
    File_List = glob.glob(path + "*.zip")

    for extractedfile in natsorted(File_List):
        with zipfile.ZipFile(extractedfile) as unzf:
            unzf.extractall(path)
    
    """ファイル編集"""
    timestamp = datetime.today()
    timename = timestamp.strftime("%Y%m%d%H%M%S")
    #パスで指定したファイルの一覧をリスト形式で取得
    csv_files = glob.glob("/home/pi/Documents/adxl355/adxl355_data/*.csv")
    #csvファイルの中身を追加していくリストを用意
    data_list = []
    #読み込むファイルのリストを走査
    for file in natsorted(csv_files):
        data_list.append(pd.read_csv(file))
    #リストを全て行方向に結合
    #axis=0:行方向に結合, sort
    df = pd.concat(data_list, axis=0, sort=True)
    df.to_csv("/home/pi/Documents/adxl355/adxl355_data/"+timename+"_total"".csv",index=False)

    print("finish " + timename)

#関数の読み出しコマンド
#schedule.every().day.at("00:00").do(EDIT)
#schedule.every(1).minutes.do(EDIT)
schedule.every(1).hour.do(EDIT)

while True:
    #定期実行の読み出し
    schedule.run_pending()
