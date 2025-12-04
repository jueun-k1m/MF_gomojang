import datetime
import json
import os

from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest
from django.contrib.staticfiles.storage import staticfiles_storage

from django.urls import path


BASE_DIR_GOMOJANG = os.path.expanduser("~/gomojang/omnitor") 
CONFIG_FILE_PATH = os.path.join(BASE_DIR_GOMOJANG, "camera_config.json")

def api_setting(request):
    handlers = {
        "GET": get_handler,
    }

    handler = handlers.get(request.method)
    if handler is None:
        return HttpResponseBadRequest("Only POST requests are allowed.")

    return handler(request)

api_path = path('calibration_api/', api_setting, name='calibration_api')

def get_handler(request):
    date_str = request.GET.get('date')
    if not date_str: return HttpResponseBadRequest("Date parameter is required.")
    image_name = f"{date_str}.jpg"
    image_relative_path = os.path.join('omnitor', 'journal_images', image_name)
    image_url = staticfiles_storage.url(image_relative_path)
    image_capture_time_str = None
    try:
        full_image_path = os.path.join(IMAGE_FILES_DIRECTORY, image_name)
        if os.path.exists(full_image_path):
            mtime = os.path.getmtime(full_image_path)
            image_capture_time = datetime.fromtimestamp(mtime)
            image_capture_time_str = image_capture_time.strftime('%H:%M:%S')
    except Exception as e:
        print(f"Error getting image mtime for {date_str}: {e}")
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
            'image_capture_time': image_capture_time_str
        })
    except FarmJournal.DoesNotExist:
        return JsonResponse({'status': 'not_found', 'image_url': image_url, 'image_capture_time': image_capture_time_str})
    except Exception as e:
        print(f"Error fetching journal entry for {date_str}: {e}")
        return JsonResponse({'status': 'error', 'message': 'Failed to retrieve journal entry.'}, status=500)

def post_handler(request):
    try:
        data = json.loads(request.body)
        date_str = data.pop('date', None)
        if not date_str:
            return HttpResponseBadRequest("Date is required to save journal entry.")

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Use YYYY-MM-DD.")

        allowed_fields = {'work', 'pesticide', 'fertilizer', 'harvest', 'notes'}
        defaults_data = {k: v for k, v in data.items() if k in allowed_fields}

        entry, created = FarmJournal.objects.update_or_create(date=date_str, defaults=defaults_data)
        message = "Journal entry updated successfully!"
        if created: message = "Journal entry created successfully!"
        print(f"Saved journal for {date_str}: {defaults_data}")
        return JsonResponse({'status': 'success', 'message': message})
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data.")
    except Exception as e:
        print(f"Error saving journal for {date_str}: {e}")
        # Provide a more generic error message to the user
        return JsonResponse({'status': 'error', 'message': 'Failed to save journal entry due to a server error.'}, status=500)
