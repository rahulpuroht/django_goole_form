from django.utils import timezone
from sr_user.models import UserProperties


class TimezoneMiddleware(object):
    def process_request(self, request):
        try:
            user = request.user
            up = UserProperties.objects.get(user = user)
            tz = up.timezone
#            print "User's TZ: ", tz
        except:
            tz = "Asia/Kolkata"
                                   
        #tz = 'Asia/Calcutta'
        if tz:
            timezone.activate(tz)
#            print "CURRENT: ", timezone.get_current_timezone()
#            print "DEFAULT: ", timezone.get_default_timezone()
