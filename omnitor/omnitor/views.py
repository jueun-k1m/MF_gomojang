import omnitor.models

# ===== 탭 1: 대시보드 =====


# 실시간 데이터를 가져오는 (1분마다)
def current_data()
	request.method == "GET"으로
	models.RawData 불러오기 -> moving_avg_filter.py
	models.CalibrationSettings 불러오기
	models.FinalData[final] = CalibrationSettings[slope]*RawData[raw] + CalibrationSettings[intercept]
		** tip_total = tip_count * tip_capacity (=5mL)
	
	
	그래서 그 FinalData를 이제 저장도 하고, 보내기도 함

# ===== 탭 2: 그래프 =====

# 과거 데이터를 가져오는
def past_data()
	사용자의 입력에 따라 date parameter를 정하기
		start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    .
    .
    .
	date parameter 안에 있는 models.FinalData들을 데이터 불러오기
	

# ===== 탭 3: 농장일지 =====

# 농장 일지 내용 저장하기
def save_journal_entry()
	request == "POST"으로 사용자의 input을 받아서 models.JournalEntry에 저장

	models.JournalEntry['farmwork'] = request.POST.get('farmwork')
	.
	.
	.

# 농장 일지 내용 불러오기
def load_journal_entry()
	달력에서 어떤 날짜를 누르면 그 날짜에 맞는 일지 내용을 DB에서 찾아서 불러오기
	try:
		entry = FarmJournal.objects.get(date=date_str)
    return JsonResponse({
	    'status': 'found',
      'farm_work': entry.farm_work,
      'pesticide': entry.pesticide,
      'fertilizer': entry.fertilizer,
      'harvest': entry.harvest,
      'notes': entry.notes,
      'image_url': image_url,
      'image_capture_time': image_capture_time
		})
	static/journal_images에서 그 날짜에 해당되는 사진 불러오기
	사진 3장 왼쪽, 오른쪽, 중앙 배치

# 카메라 지정 시간마다
def capture_journal_image()
	models.JournalEntry['capture_time']으로 지정 시간 불러오기
	지정 시간 scheduling 사용 (그 시간마다 이 코드를 실행)
	시간이 되면 :
		1. 사진 하나 찍고 오늘의날짜_C.jpg 이런 식으로 중앙 사진이라고 라벨 후 저장
		2. 아두이노 arduino.py (command == '1') 보내서 카메라 고정 풀고
		3. 아두이노 arduino.py (command == '3') 보내서 왼쪽으로 회전
		4. 조금 기다렸다가 사진 찍고 {todays_date}_L.jpg 저장
		5. 아두이노 arduino.py (command == '4') 보내서 오른쪽으로 회전
		6. 사진 찍고 _R.jpg 저장
		7. 아두이노 arduino.py (command == '3') 으로 다시 중앙으로
		8. 아두이노 arduino.py (command == '2') 보내서 카메라 고정
		
def save_capture_time()
	request == "POST"로 사용자가 capture_time 시간을 보냈다면 
	-> 그걸 이제 models.JournalEntry['capture_time']에 저장하도록
	

# ===== 탭 4: 보정 설정 =====

def calibration_api(){

	request == "POST"로 사용자가:
		1. weight real1, real2를 넣었다면,
			models.RawData에서 <weight_raw>를 moving_avg_filter 적용 후 filtered1, filtered2에 저장
			calibration.py에다 real1, real2, filtered1, filtered2 변수 보내기
				(calibration.py에서 그걸 계산해서 models.CalibrationSettings에 저장)
				
				
# ===== LCD 디스플레이 =====

def display()
	models.FinalData에서 무게, 급액량, 온도, 습도를 받아오기
	LCDdisplay.py에다 보내기
	ErrorCode도 보내서 만약에 ErrorCode != NULL이면 (default=NULL로 두기), # 우선 순위로 에러부터 보여주도록 코드 짜기
		그 ErrorCode부터 프린트 하도록 하기
