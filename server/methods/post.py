import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.event_sorter import sort_event
from handlers.photos_handler import process_photo_event

def PostMethod(request, executor):
    print("POST request received.")
    print("Headers:", request.headers)
    print("Body:", request.get_json())
    
    event = request.get_json()
    
    # Sort the event and process asynchronously
    if event:
        outp = sort_event(event)
        if outp == "photo":
            executor.submit(process_photo_event, event)
        executor.submit(sort_event, event)
        return "Event sorting initiated", 200
    
    return "Invalid event", 400