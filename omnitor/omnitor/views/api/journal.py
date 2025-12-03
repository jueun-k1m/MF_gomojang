
from models import JournalEntry

def get_handler(request):
    return JournalEntry.objects.all().order_by('-created_at')


def post_handler(request, data):
    entry = JournalEntry(
        title=data.get('title', ''),
        content=data.get('content', ''),
    )
    entry.save()
    return entry


