
from django.contrib import admin
from django.urls import path
from app.views import home, testApi, postFile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('apitest/', testApi, name="api-test"),
    path('api/', postFile, name="api-post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
