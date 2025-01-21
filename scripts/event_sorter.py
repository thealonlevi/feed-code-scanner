
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
                    return change['value'], "photo"
                else:
                    print(f"Unhandled event type: {item_type}")
                    return event, "Unknown"
    except Exception as e:
        print(f"Error sorting event: {e}")
        return event, "Unknown"
