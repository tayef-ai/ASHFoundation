from .models import Setting, Region

def my_custom_context(request):
    r = Region.objects.get(name='Bangladesh')
    query = Setting.objects.get(region=r)
    return {'my_data': query}
