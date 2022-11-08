from django import template
import pytz

register = template.Library()

@register.filter(name="convert")
def convert(date):
    local_tz = pytz.timezone("Europe/London")
    converted = date.replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%d/%m/%Y - %H:%M")
    return str(converted)