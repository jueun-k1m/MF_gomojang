import os
import sys
import time
import django
import threading
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__)) # service 폴더
root_dir = os.path.dirname(current_dir) # 한 단계 위 dir

sys.path.append(root_dir) # ★ 루트 경로를 추가해야 'devices'와 'omnitor'를 찾음

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omnitor.settings")
django.setup()

from omnitor.models import RawData # DB 모델
from django.db import connection   # DB 연결 관리용
from devices.arduino import SerialSingleton

def sensor_loop():
    arduino = SerialSingleton.instance()

    arduino.start()

    while True:
        try:
            data = arduino.get_current_data()

            if data:
                RawData.objects.create(
                    timestamp=datetime.now(),
                    air_temperature=data.air_temperature,
                    air_humidity=data.air_humidity,
                    co2=data.co2,
                    insolation=data.insolation,
                    weight_raw=data.weight_raw,
                    ph_voltage=data.ph_voltage,
                    ec_voltage=data.ec_voltage,
                    water_temperature=data.water_temperature,
                    tip_count=data.tip_count
                )

                connection.close()
            else:
                pass
            time.sleep(1)
        
        except Exception as e:
            print(f"[Arduino Service] 오류 발생: {e}")
            time.sleep(1)

        except KeyboardInterrupt:
            break
    arduino.stop()

if __name__ == '__main__':
    sensor_loop()
