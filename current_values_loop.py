import time  #タイムカウントに使用するライブラリ
import datetime  #タイムスタンプに使用するライブラリ
import numpy as np  #配列計算、FFT化する時に使用するライブラリ
import csv  #csvを作成するライブラリ
import matplotlib  #グラフ処理に用いるライブラリ
matplotlib.use('agg')
import matplotlib.pyplot as plt
#t00 = time.time()
import sys  #ファイルを読み出したい時に使用するライブラリ
sys.path.append('/home/pi/Documents/adxl355/')
from adxl355 import ADXL355  # pylint: disable=wrong-import-position
device = ADXL355()            # pylint: disable=invalid-name
#t0 = time.time()
#print(t0-t00)

X = []
Y = []
Z = []
N = 4096
dt = 0.001
overrun = 2048
#t1 = time.time()
index=0
while index < N:
    axes = device.get_axes()  # pylint: disable=invalid-name
    X.append(axes[0])
    Y.append(axes[1])
    Z.append(axes[2])
    #time.sleep(0.0001)
    index += 1
#t2 = time.time()
#print(t2-t1)

while True:
    #t3 = time.time()
    axes = device.get_axes()  # pylint: disable=invalid-name
    if axes[0] < 1.8 or axes[1] < 1.8 or axes[2] < 1.8:
        X.append(axes[0])
        X.pop(0)
        Y.append(axes[1])
        Y.pop(0)
        Z.append(axes[2])
        Z.pop(0)
    elif axes[0] >= 1.8 or axes[1] >= 1.8 or axes[2] >= 1.8:
        X.append(axes[0])
        X.pop(0)
        Y.append(axes[1])
        Y.pop(0)
        Z.append(axes[2])
        Z.pop(0)
        i = 0
        while i < overrun:
            axes = device.get_axes()
            X.append(axes[0])
            X.pop(0)
            Y.append(axes[1])
            Y.pop(0)
            Z.append(axes[2])
            Z.pop(0)
            i += 1
        XG = X
        YG = Y
        ZG = Z
        #時間軸
        t = np.arange(0, N*dt, dt)  #(開始、終了、分割数)
        #周波数軸
        freq = np.linspace(0, 1.0/dt, N)  #(開始、終了、分割数)
        #X軸のFFT化
        FX = np.fft.fft(XG)
        FX_abs = np.abs(FX)  #絶対値に換算
        FX_abs_amp = FX_abs/N*2
        FX_abs_amp[0] = FX_abs_amp[0]/2
        #Y軸のFFT化
        FY = np.fft.fft(YG)
        FY_abs = np.abs(FY)
        FY_abs_amp = FY_abs/N*2
        FY_abs_amp[0] = FY_abs_amp[0]/2
        #Z軸のFFT化
        FZ = np.fft.fft(ZG)
        FZ_abs = np.abs(FZ)
        FZ_abs_amp = FZ_abs/N*2
        FZ_abs_amp[0] = FZ_abs_amp[0]/2
        #グラフ化
        #１つ目。加速度の時系列グラフ
        fig = plt.figure(figsize=(12,6))
        ax2 = fig.add_subplot(2,3,1)
        plt.xlabel('time(sec)',fontsize=12)
        plt.ylabel('acceleration(G)',fontsize=12)
        plt.plot(t,XG, label = 'X')
        plt.plot(t,YG, label = 'Y')
        plt.plot(t,ZG, label = 'Z')
        plt.legend(loc = 'center right')
        plt.ylim(-2, 2)  #y軸のレンジ
        #2つ目。FFTグラフ。3軸重ね合わせ
        ax2 = fig.add_subplot(2,3,3)
        plt.xlabel('freqency(Hz)',fontsize=12)
        plt.ylabel('amplitude',fontsize=12)
        #鏡像ピーク分を除去する。（ナイキスト定数）
        plt.plot(freq[:int(N)+1],FX_abs_amp[:int(N)+1])
        plt.plot(freq[:int(N)+1],FY_abs_amp[:int(N)+1])
        plt.plot(freq[:int(N)+1],FZ_abs_amp[:int(N)+1])
        plt.plot(t,XG, label = 'X', color = 'blue')
        plt.plot(t,YG, label = 'Y', color = 'darkorange')
        plt.plot(t,ZG, label = 'Z', color = 'green')
        plt.legend(loc = 'center right')
        plt.axis([0,1/dt/2,0,0.5])  #x,y軸のレンジ固定
        #3つ目。FFTグラフ。x軸
        ax3 = fig.add_subplot(2,3,4)
        plt.xlabel('X.freqency(Hz)',fontsize=12)
        plt.ylabel('amplitude',fontsize=12)
        plt.plot(freq[:int(N)+1],FX_abs_amp[:int(N)+1],color = 'blue')
        plt.axis([0,1/dt/2,0,0.5])  #x,y軸のレンジ固定
        #4つ目。FFTグラフ。y軸
        ax3 = fig.add_subplot(2,3,5)
        plt.xlabel('Y.freqency(Hz)',fontsize=12)
        plt.ylabel('amplitude',fontsize=12)
        plt.plot(freq[:int(N)+1],FY_abs_amp[:int(N)+1],color = 'darkorange')
        plt.axis([0,1/dt/2,0,0.5])  #x,y軸のレンジ固定
        #5つ目。FFTグラフ。z軸
        ax3 = fig.add_subplot(2,3,6)
        plt.xlabel('Z.freqency(Hz)',fontsize=12)
        plt.ylabel('amplitude',fontsize=12)
        plt.plot(freq[:int(N)+1],FZ_abs_amp[:int(N)+1],color = 'green')
        plt.axis([0,1/dt/2,0,0.5])  #x,y軸のレンジ固定
        fig.subplots_adjust(wspace=0.3,hspace=0.3)  #隣接グラフとの隙間
        #グラフの図、CSVファイルの出力
        dt_now = datetime.datetime.now()
        filename = str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) + str(dt_now.minute) + str(dt_now.second)
        plt.savefig('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.png')
        print('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.png', 'saved')
        #csvに書き込み(w)、出力する(f)
        with open('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows([X, Y, Z])
        print('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'saved')
        #t4 = time.time()
        #print(t4-t3)
