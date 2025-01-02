from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "Alhaj Shamsul Hoque Foundation"
admin.site.site_title = "Alhaj Shamsul Hoque Foundation"
admin.site.index_title = "Alhaj Shamsul Hoque Foundation"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hospital/', include('ahospital.urls')),
    path('', include('aashfApp.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)