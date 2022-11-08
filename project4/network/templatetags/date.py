from django import template
from math import floor
import time
from datetime import datetime
import pytz
register = template.Library()
@register.filter(name="timeSince")
def timeSince(date):
    local_tz = pytz.timezone("Europe/London")
    converted =  date.replace(tzinfo=pytz.utc).astimezone(local_tz)
    postDate = time.mktime(datetime.strptime(str(converted), "%Y-%m-%d %H:%M:%S.%f%z").timetuple())
    currentDate = time.time()
    if (currentDate - postDate) < 60:       
        return "Just now"
    elif (currentDate - postDate)/60 < 60:
        return f"{floor((currentDate - postDate)/60)}m"
    elif (currentDate - postDate)/60/60 < 24:    
        return f"{floor((currentDate - postDate)/60/60)}h"
    else: return f"{floor((currentDate - postDate)/60/60/24)}d"

