
window_size = 5

from collections import deque

from omnitor.models import RawData

data = [
    'air_temperature',
    'air_humidity',
    'co2',
    'insolation',
    'weight_raw',
    'ph_voltage',
    'ec_voltage',
    'water_temperature',
    'tip_count',
    'soil_temperature',
    'soil_humidity',
    'soil_ec',
    'soil_ph'
]

def moving_avg_filter(window_size=5):
    """
    호출되는 순간 DB에서 최신 window_size개를 가져와 평균을 계산하여 반환
    """
    # DB에서 가장 최신 데이터 N개를 가져옴
    latest_records = list(RawData.objects.all().order_by('-created_at').values(*data)[:window_size])

    # 데이터가 하나도 없으면 빈 딕셔너리 반환
    if not latest_records:
        return {key: None for key in data}

    filtered_result = {}

    # 각 센서 항목별로 평균 계산
    for key in data:
        # None이 아닌 값들만 필터링
        valid_values = [
            record[key] for record in latest_records 
            if record.get(key) is not None
        ]

        if valid_values:
            # 평균 계산
            filtered_result[key] = sum(valid_values) / len(valid_values)
        else:
            # 유효한 값이 없으면 None
            filtered_result[key] = None

    return filtered_result


def high_pass_filter():
    """
    min threshold 이상인 값만 통과시키는 필터
    """

def low_pass_filter():
    """
    max threshold 이하인 값만 통과시키는 필터
    """
