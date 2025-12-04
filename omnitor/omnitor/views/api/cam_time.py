from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from datetime import datetime

from models import FarmJournal


def get_handler(request):
    
    return JsonResponse({'status': 'success', 'capture_time': FarmJournal.cam_time})

def post_handler(request):
        try:
            data = json.loads(request.body)
            new_time = data.get('capture_time') 
            
            if not new_time:
                return HttpResponseBadRequest("Time is required.")

            # 시간 형식 검증 (HH:MM)
            datetime.strptime(new_time, '%H:%M')

            # DB에 저장
            FarmJournal.camera_capture_time = new_time
            FarmJournal.save()
            
            print(f"Camera capture time updated to: {new_time}")
            return JsonResponse({'status': 'success', 'message': f'촬영 시간이 {new_time}으로 설정되었습니다.'})

        except ValueError:
            return HttpResponseBadRequest("Invalid time format (HH:MM).")
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return HttpResponseBadRequest("Method not allowed.")
