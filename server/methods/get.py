def GetMethod(request, VERIFY_TOKEN):
    print("GET request received.")
    print("Headers:", request.headers)
    print("Query Parameters:", request.args)
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403