def customer_processor(request):
    return {"current_customer": request.user.userprofile.customer}
