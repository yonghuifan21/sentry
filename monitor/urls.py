from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('monitor/', include('monitor.urls')),
    path('admin/', admin.site.urls),
]