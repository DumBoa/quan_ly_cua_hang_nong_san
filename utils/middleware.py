from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/accounts/login') or path.startswith('/static'):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        return self.get_response(request)