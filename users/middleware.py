from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings

class UserInactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            last_activity = request.session.get('last_activity')
            if last_activity:
                inactive_time = timezone.now() - timezone.datetime.fromtimestamp(last_activity)
                if inactive_time.seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
            request.session['last_activity'] = timezone.now().timestamp()

        response = self.get_response(request)
        return response