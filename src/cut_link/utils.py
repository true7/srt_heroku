import string
import random
import json
from calendar import month_name
from django.conf import settings

SHORTLINK_MIN = getattr(settings, "SHORTLINK_MIN", 6)


def code_generator(size=SHORTLINK_MIN):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def create_shortlink(instance):
    new_link = code_generator()
    class_ = instance.__class__
    query_set = class_.objects.filter(shortlink=new_link)
    if query_set.exists():
        return create_shortlink()
    return new_link


def json_data_func(instance):
    ''' Return json format data, ready for passing into AmCharts.
        Contains 2 items - name of the month and count of distinct
        links, which were cut on the website.
    '''
    class_ = instance.__class__
    # FIXME. The problem is every next year it will add results above
    result = []
    for month in range(1, len(month_name)):
        count_use = class_.objects.filter(pub_date__month=month).count()
        data = dict(month=month_name[month], count=count_use)
        result.append(data)
    json_data = json.dumps(result)
    return json_data
