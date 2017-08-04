def customer_processor(request):
    if request.user.is_authenticated():
        return {"current_customer": request.user.userprofile.customer}
    return {"current_customer": None}
