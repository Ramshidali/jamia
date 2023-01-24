from datetime import datetime
from django import template

from institution.models import InstitutionEvents

register = template.Library()

@register.simple_tag
def get_event_status(pk):
    if InstitutionEvents.objects.filter(pk=pk,is_deleted=False).exists():
        date_status = InstitutionEvents.objects.get(pk=pk,is_deleted=False)
        today = datetime.datetime.today()
        if date_status.date>=today :
            date_status = True
        return date_status