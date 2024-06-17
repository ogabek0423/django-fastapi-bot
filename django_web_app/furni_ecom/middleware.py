class MethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '_method' in request.POST:
            method = request.POST['_method'].upper()
            if method in ['PUT', 'DELETE']:
                request.method = method
                request.META['REQUEST_METHOD'] = method
        return self.get_response(request)
