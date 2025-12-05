import os
import sys
import math
from datetime import datetime
import django
from omnitor.models import CalibrationSettings, FinalData, RawData

def save_final_data(filtered_data):
    """
    필터링 된 데이터에 보정 설정을 적용하여 FinalData DB에 최종 데이터를 저장
    """

    if not filtered_data:
        return None
        

    FinalData.objects.create(
        timestamp=RawData.timestamp,
        air_temperature=filtered_data['air_temperature'],
        air_humidity=filtered_data['air_humidity'],
        co2=filtered_data['co2'],
        insolation=filtered_data['insolation'],
        weight=CalibrationSettings.weight_slope * filtered_data['weight'] + CalibrationSettings.weight_intercept,
        water_temperature=filtered_data['water_temperature'],
        ph=(CalibrationSettings.ph_slope * filtered_data['ph']) + CalibrationSettings.ph_intercept,
        ec=(CalibrationSettings.ec_slope * filtered_data['ec']) + CalibrationSettings.ec_intercept,
        soil_temperature=filtered_data['soil_temperature'],
        soil_humidity=filtered_data['soil_humidity'],
        soil_ec=filtered_data['soil_ec'],
        soil_ph=filtered_data['soil_ph']
    )
