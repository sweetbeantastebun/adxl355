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

device.write_data(0x28, 0x02)
#print("filter_setting", device.read_data(0x28))
#print("POWER_CTL", device.read_data(0x2D))
#print("TEMP2", device.read_data(0x06))
#print("TEMP1", device.read_data(0x07))
Temperature_Response = device.read_data(0x06) <<8 | device.read_data(0x07)
Temperature = (Temperature_Response - 1852) / (-9.05) + 25
print("Temperature[degC]", int(Temperature))
#device.write_data(0x1E, 0x01)
#device.write_data(0x1F, 0x01)
#print("OFFSET_X_H", device.read_data(0x1E))
#print("OFFSET_X_L", device.read_data(0x1F))

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
    #device.write_data(0x28, 0x02)
    #print("filter_setting", device.read_data(0x28))
    N = 512
    #overrun = 2048
    index=0
    while index < N:
        axes = device.get_axes()  # pylint: disable=invalid-name
        X.append(axes[0])
        Y.append(axes[1])
        Z.append(axes[2])
        index += 1
        time.sleep(0.0007)
        t2 = time.time()

def data_analysis():
    global t3
    global t4
    global t5
    global t6
    t3 = time.time()
    timestamp = datetime.today()
    filename = timestamp.strftime("%Y%m%d%H%M%S")
    dt = 0.001 #サンプリングレート0.5msec(1000Hz)
    #dt = 0.000025
    
    #時間軸(サンプル数)
    #t = np.arange(0, N*dt, dt)  #(開始、終了、分割数)
    pcs = np.arange(0, N)

    #FFT
    #X軸
    #FFT_X = np.fft.fft(X)
    #samples = 256  #サンプル数を指定 #256データの周波数分解能は4Hz
    #FFT_X = np.fft.fft(X[0:samples])  #2次元配列(実部，虚部)
    #FFT_X = FFT_X[:int(FFT_X.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    #Y軸
    #FFT_Y = np.fft.fft(Y)
    #samples = 256  #サンプル数を指定 #256データの周波数分解能は4Hz
    #FFT_Y = np.fft.fft(Y[0:samples])  #2次元配列(実部，虚部)
    #FFT_Y = FFT_Y[:int(FFT_Y.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    #Z軸
    #FFT_Z = np.fft.fft(Z)
    samples =512  #サンプル数を指定 #256データの周波数分解能は4Hz
    FFT_Z = np.fft.fft(Z[0:samples])  #2次元配列(実部，虚部)
    FFT_Z = FFT_Z[:int(FFT_Z.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    #周波数軸
    frequency = np.linspace(0, 1.0/dt, samples)  #(開始、終了、分割数)
    frequency = frequency[:int(frequency.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除 
    #print("frequency",len(frequency))
    t4 = time.time()

    #グラフ化
    plt.ion()
    plt.clf()
    #１つ目。加速度の時系列グラフ:X-axis
    #plt.subplot(2, 3, 1)
    #plt.plot(pcs,X, label = "X", color = "blue")
    #plt.xlabel("Sample Number.X-axis(pcs)", fontsize = 8)
    #plt.ylabel("acceleration(G)", fontsize = 8)
    #plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    #plt.axis([0, N, -6,6])
    #plt.xticks(fontsize = 7)
    #plt.yticks(fontsize = 7)
    #plt.grid(which = "both")
    #2つ目。加速度の時系列グラフ:Y-axis
    #plt.subplot(2, 3, 2)
    #plt.plot(pcs,Y, label = "Y", color = "darkorange")
    #plt.xlabel("Sample Number.Y-axis(pcs)", fontsize = 8)
    #plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    #plt.axis([0, N, -6,6])
    #plt.xticks(fontsize = 7)
    #plt.yticks(fontsize = 7)
    #plt.grid(which = "both")
    #加速度の時系列グラフ:Z-axis
    plt.subplot(2, 1, 1)
    plt.plot(pcs,Z, label = "Z", color = "blue")
    plt.xlabel("Sample Number.Z-axis(pcs)", fontsize = 8)
    plt.ylabel("acceleration(G)", fontsize = 8)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    plt.axis([0, N, -6,6])
    plt.xticks(fontsize = 7)
    plt.yticks(fontsize = 7)
    plt.grid(which = "both")
    
    #4つ目。FFTグラフ。X-axis
    #plt.subplot(2, 3, 4)
    #plt.plot(frequency, np.abs(FFT_X), label = "X", color = "blue")
    #plt.xlabel("freqency.X-axis(Hz)", fontsize=8)
    #plt.ylabel('amplitude_spectrum',fontsize=8)
    #plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    #plt.axis([0,1/dt/2, 0.001,1000])  #x,y軸のレンジ固定
    #plt.axis([0,1/dt/2, 0,100])  #x,y軸のレンジ固定
    #plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    #plt.xticks(fontsize = 7)
    #plt.yticks(fontsize = 7)
    #plt.grid(which="both")
    #plt.yscale("log")
    #5つ目。FFTグラフ。Y-axis
    #plt.subplot(2, 3, 5)
    #plt.plot(frequency, np.abs(FFT_Y), label = "Y", color = "darkorange")
    #plt.xlabel("freqency.Y-axis(Hz)", fontsize=8)
    #plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    #plt.axis([0,1/dt/2, 0.001,1000])  #x,y軸のレンジ固定
    #plt.axis([0,1/dt/2, 0,100])  #x,y軸のレンジ固定
    #plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    #plt.xticks(fontsize = 7)
    #plt.yticks(fontsize = 7)
    #plt.grid(which="both")
    #plt.yscale("log")
    #FFTグラフ。Z-axis
    y_axis_range_min = 0
    y_axis_range_max = 100
    plt.subplot(2, 1, 2)
    plt.plot(frequency, np.abs(FFT_Z), label = "Z", color = "blue")
    plt.xlabel("freqency.Z-axis(Hz)", fontsize=8)
    plt.ylabel('amplitude_spectrum',fontsize=8)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper right", borderaxespad = 0, fontsize = 8)
    #plt.axis([0,1/dt/2, 0.001,1000])  #x,y軸のレンジ固定
    plt.axis([0,1/dt/2, y_axis_range_min,y_axis_range_max])  #x,y軸のレンジ固定
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.xticks(fontsize = 7)
    plt.yticks(fontsize = 7)
    plt.grid(which="both")
    #plt.xscale("log")
    
    #グラフ出力
    #plt.savefig('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.png')
    plt.draw()
    plt.pause(0.1)
    
    #plt.show()
    #plt.close()
    
    #csvに書き込み(w)、出力する(f)
    #with open('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'w', newline='', encoding="utf-8") as f:
        #writer = csv.writer(f, lineterminator="\n")
        #writer.writerows([X, Y, Z])
    #print('/home/pi/Documents/adxl355/adxl355_data/'+filename+'.csv', 'saved')
    t5 = time.time()

    #text出力
    #np.savetxt('/home/pi/Documents/adxl355/adxl355_data/'+filename+'frequency', frequency, delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/adxl355/adxl355_data/'+filename+'amplitude', np.abs(FFT_Z), delimiter = " ", fmt='%.4f')
    #Temperature_Response = device.read_data(0x06) <<8 | device.read_data(0x07)
    #Temperature = (Temperature_Response - 1852) / (-9.05) + 25
    #print("Temperature[degC]", int(Temperature))
    t6 = time.time()

#data_collection()
#data_analysis()

while True:
    data_collection()
    data_analysis()
    print("t2-t1", t2-t1)
    #print("t6-t3", t6-t3)
