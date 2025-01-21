import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from handlers.photos_handler import process_photo_event

def sort_event(event):
    """
    Sort the event and route it to the appropriate handler.
    """
    try:
        for entry in event.get("entry", []):
            for change in entry.get("changes", []):
                item_type = change.get("value", {}).get("item")
                
                if item_type == "photo":
                    print("Photo event detected. Routing to photo handler...")
                    process_photo_event(change["value"])
                else:
                    print(f"Unhandled event type: {item_type}")
    except Exception as e:
        print(f"Error sorting event: {e}")
