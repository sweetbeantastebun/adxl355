"""ADXL355 Python library for NanoPi.
This module implements basic operations for ADXL355
accelerometer chip for NanoPi
"""
import spidev
# ADXL355 constants
# SPI config
SPI_MAX_CLOCK_HZ = 10000000  #クロック周波数10MHz
SPI_MODE = 0b00  
SPI_BUS = 1  #SPI1に接続
SPI_DEVICE = 0  #加速度センサのID

#Addresses,レジスタの構成をアサイン
XDATA3 = 0x08  #X軸
XDATA2 = 0x09
XDATA1 = 0x0A
YDATA3 = 0x0B  #Y軸
YDATA2 = 0x0C
YDATA1 = 0x0D
ZDATA3 = 0x0E  #Z軸
ZDATA2 = 0x0F
ZDATA1 = 0x10
RANGE = 0x2C  #測定範囲を選択するレジスタ
POWER_CTL = 0x2D  #測定モードを有効するレジスタ

# Data Range
RANGE_2G = 0x01
RANGE_4G = 0x02
RANGE_8G = 0x03

# Values
READ_BIT = 0x01
WRITE_BIT = 0x00
DUMMY_BYTE = 0x00
MEASURE_MODE = 0x06  #Only accelerometer

class ADXL355:
    """
    クラス作成
    加速度センサの読み込み、書き込み、データ取得の定義
    """
    def __init__(self, measure_range=RANGE_2G):
        # SPI init
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_CLOCK_HZ
        self.spi.mode = SPI_MODE

        # Device init
        self._set_measure_range(measure_range)
        self._enable_measure_mode()

    def write_data(self, address, value):
        #ADXL355のデバイスアドレスの書き込み設定するため
        #INI値のaddressとvalueのアドレス指定。
        #アドレス書き込み関数の指定。
        #最初にアドレスビットを送信
        #その後にデータビットを送信する。
        device_address = address << 1 | WRITE_BIT
        self.spi.xfer2([device_address, value])
        #spi.xfer2:CS制御を通信する関数。spidevの定義文。

    def read_data(self, address):
        #アドレス読み出し関数の指定。
        device_address = address << 1 | READ_BIT
        return self.spi.xfer2([device_address, DUMMY_BYTE])[1]

    def read_multiple_data(self, address_list):
        #複数バイトの読み出し。
        #始めの１バイトで読み出したいレジスタ0x08（XDATA3）を
        spi_ops = [0x11,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        return self.spi.xfer2(spi_ops)[1:]
        #0x11は0x08をReadコマンドにした値。0x08<<1|0x01

    def _set_measure_range(self, measure_range):
        #測定レンジの書き込み設定
        self.write_data(RANGE, measure_range)

    def _enable_measure_mode(self):
        #測定モードにする
        self.write_data(POWER_CTL, MEASURE_MODE)

    def get_axes(self):
        #測定データの読み出し、加速度への出力
        # Reading data
        raw_data = self.read_multiple_data(
            [XDATA3, XDATA2, XDATA1, YDATA3, YDATA2, YDATA1, ZDATA3, ZDATA2, ZDATA1]
        )
        #戻り値を格納
        x_data = raw_data[0:3]  #スライス演算[1,2,3]
        y_data = raw_data[3:6]  #スライス演算[4,5,6]
        z_data = raw_data[6:9]  #スライス演算[7,8,9]
        #print(raw_data[0:3])

        # Join data
        x_data = (x_data[2] >> 4) + (x_data[1] << 4) + (x_data[0] << 12)
        y_data = (y_data[2] >> 4) + (y_data[1] << 4) + (y_data[0] << 12)
        z_data = (z_data[2] >> 4) + (z_data[1] << 4) + (z_data[0] << 12)
        #print(x_data)

        # Apply two complement
        #2の補数フォーマット20ビットデータ
        #もし0x80000以上は負の数
        if x_data & 0x80000 == 0x80000:
            x_data = x_data - 2**20
        if y_data & 0x80000 == 0x80000:
            y_data = y_data - 2**20
        if z_data & 0x80000 == 0x80000:
            z_data = z_data - 2**20

        #加速度に換算。小数点データにしたいためflaot型にする。-3.9μG/LSB
        accX = float(x_data) * -3.9 / 1000000
        accY = float(y_data) * -3.9 / 1000000
        accZ = float(z_data) * -3.9 / 1000000
        #print(accX)

        # Return values
        return [accX, accY, accZ]
