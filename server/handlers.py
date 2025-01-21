def handle_webhook_event(event):
    """
    Handle and log the incoming webhook event.
    """
    try:
        # Log the received event for debugging
        print("Received Webhook Event:", event)
        return {"status": "success", "message": "Event received successfully"}
    except Exception as e:
        print(f"Error handling webhook event: {e}")
        return {"status": "error", "message": str(e)}
