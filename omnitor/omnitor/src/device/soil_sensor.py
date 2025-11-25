import os
import sys
import serial
import time
import statistics
import minimalmodbus
import serial.tools.list_ports
from collections import deque
from datetime import datetime

from omnitor.models import RawData


# 변수 설정
modbus_baudrate = 4800

save_data_sec = 1 # 데이터 저장하는 초 단위
read_data_sec = 0.5 # 데이터 읽는 초 단위


def find_modbus_port():

    """ USB 포트에서 토양 센서 (RS485 -> USB 동글 연결) 포트 찾는 함수 """

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Serial" in port.description:
            modbus_port = port.device
            return modbus_port
    return None


def read_data(instrument):

    """ 토양 센서 데이터 읽기 함수 """

    try:
        modbus_data = instrument.read_registers(0, 4, 3)

        data = {
            'timestamp': datetime.now(),
            'soil_temperature': modbus_data[1] / 10.0,      # 단위: 0.1°C 
            'soil_humidity': modbus_data[0] / 10.0,         # 단위: 0.1% 
            'soil_ec': modbus_data[2] / 1.0,                # 단위: 1 us/cm,
            'soil_ph': modbus_data[3] / 10.0                # 단위: 0.1 
         }
        return data

    except Exception as e:
        print(f"데이터 읽기 중 에러 발생: {e}")


def save_to_database(data):

    """ 데이터베이스에 데이터 저장 함수 """
    try:
        
        RawData.objects.create(
            soil_temperature=data['soil_temperature'],
            soil_humidity=data['soil_humidity'],
            soil_ph=data['soil_ph'],
            soil_ec=data['soil_ec'],
        )
    except Exception as e:
        print(f"데이터베이스 저장 중 에러 발생: {e}")

def main():

    """ 메인 함수 """
    """ 토양 센서 시리얼 포트 열기 및 데이터 읽기 """

    print("토양 센서 읽기 시작합니다.")

    instrument = None

    last_save_time = time.time()
    last_read_time = time.time()


    while True:

        try:
            current_time = time.time()

            if instrument is None:
                modbus = find_modbus_port()

                if modbus:
                    try:
                        instrument = minimalmodbus.Instrument(modbus, 1, mode='rtu') # MODBUS 연결
                        instrument.serial.baudrate = modbus_baudrate  
                        instrument.serial.bytesize = 8
                        instrument.serial.parity = serial.PARITY_NONE
                        instrument.serial.stopbits = 1
                        instrument.serial.timeout = 1  
                        instrument.close_port_after_each_call = True

                        time.sleep(2)  # 연결 안정화 대기
                        
                        if instrument:
                            print(f"토양 센서 연결 성공: {modbus}")
                        else:
                            instrument = None
                    except Exception as e:
                        print(f"토양 센서 연결 실패: {e}")
                        instrument = None
                else:
                    print("토양 센서 포트를 찾지 못 했습니다. 다시 시도합니다...")
                    instrument = None

                continue

            if current_time - last_read_time >= read_data_sec:
                data = read_data(instrument) # 데이터 읽기
                if data:
                    last_read_time = current_time
            if current_time - last_save_time >= save_data_sec:
                save_to_database(data) # 데이터베이스에 저장
                last_save_time = current_time
        except Exception as e:
            print(f"메인 루프 중 에러 발생: {e}")

        time.sleep(0.05)  # CPU 사용량 절감을 위한 짧은 대기
                

if __name__ == '__main__':
    main()
