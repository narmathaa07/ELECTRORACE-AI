def chat_response(query):

    query = query.lower()

    if "save" in query:
        return "Reduce AC usage by 1 hour/day → save RM15/month"

    if "bill" in query:
        return "Estimated bill is RM 180 based on current usage"

    if "waste" in query:
        return "Main energy waste: Air Conditioner usage during empty rooms"

    if "tip" in query:
        return "Turn off idle appliances and reduce standby power loss"

    return "Ask about bill, savings, waste, or prediction"
