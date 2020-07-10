import time  #タイムカウントに使用するライブラリ
from datetime import datetime  #タイムスタンプに使用するライブラリ
import numpy as np  #配列計算、FFT化する時に使用するライブラリ
import csv  #csvを作成するライブラリ
import matplotlib.pyplot as plt
import sys  #ファイルを読み出したい時に使用するライブラリ
sys.path.append('/home/pi/Documents/adxl355/')
from adxl355 import ADXL355  # pylint: disable=wrong-import-position
device = ADXL355()            # pylint: disable=invalid-name
#t0 = time.time()

def data_collection():
    global t1
    global t2
    global N
    global X
    global Y
    global Z
    t1 = time.time()
    X = []
    Y = []
    Z = []
    N = 4096
    #overrun = 2048
    index=0
    while index < N:
        axes = device.get_axes()  # pylint: disable=invalid-name
        X.append(axes[0])
        Y.append(axes[1])
        Z.append(axes[2])
        index += 1
        t2 = time.time()

def data_analysis():
    timestamp = datetime.today()
    filename = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)
    dt = 0.001 #サンプリングレート1msec
    #dt = 0.000025
    
    #時間軸(サンプル数)
    #t = np.arange(0, N*dt, dt)  #(開始、終了、分割数)
    pcs = np.arange(0, N)

    #Z軸のFFT化
    #FFT_Z = np.fft.fft(Z)
    samples = 256  #サンプル数を指定 #256データの周波数分解能は4Hz
    FFT_Z = np.fft.fft(Z[0:samples])  #2次元配列(実部，虚部)
    FFT_Z = FFT_Z[:int(FFT_Z.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    #周波数軸
    frequency = np.linspace(0, 1.0/dt, samples)  #(開始、終了、分割数)
    frequency = frequency[:int(frequency.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除 
    #print("frequency",len(frequency))
    t3 = time.time()

    #グラフ化
    plt.ion()
    plt.clf()
    #１つ目。加速度の時系列グラフ
    plt.subplot(2, 1, 1)
    plt.xlabel('Number(pcs)',fontsize=8)
    plt.ylabel('acceleration(G)',fontsize=8)
    plt.plot(pcs,X, label = 'X')
    plt.plot(pcs,Y, label = 'Y')
    plt.plot(pcs,Z, label = 'Z')
    plt.legend(loc = 'center right')
    plt.axis([0, N, -2,2])
    plt.grid(which="both")
    #2つ目。FFTグラフ。z軸
    plt.subplot(2, 1, 2)
    plt.plot(frequency,np.abs(FFT_Z),color = 'green')
    plt.xlabel('freqency.Z-axis(Hz)',fontsize=8)
    plt.ylabel('amplitude',fontsize=8)
    plt.axis([0,1/dt/2, 0.001,1000])  #x,y軸のレンジ固定
    plt.subplots_adjust(wspace=0.3,hspace=0.3)  #隣接グラフとの隙間
    plt.grid(which="both")
    plt.yscale("log")
    #グラフ出力
    #plt.savefig('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.png')
    plt.draw()
    plt.pause(0.1)
    #plt.close()
    
    #csvに書き込み(w)、出力する(f)
    #with open('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'w', newline='', encoding="utf-8") as f:
        #writer = csv.writer(f, lineterminator="\n")
        #writer.writerows([X, Y, Z])
    #print('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'saved')
    t4 = time.time()

    #text出力
    #np.savetxt('/home/pi/Documents/adxl355/adxl355_data/'+filename+'frequency', frequency, delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/adxl355/adxl355_data/'+filename+'amplitude', np.abs(FFT_Z), delimiter = " ", fmt='%.4f')
    t5 = time.time()

while True:
    data_collection()
    data_analysis()
    print("t2-t1",t2-t1)
