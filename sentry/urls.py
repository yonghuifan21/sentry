"""sentry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

import monitor.views
from . import views
from . import viewstest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('warning/<int:type>/', csrf_exempt(views.warningParse), name='warningParse'),
    path('warning-test/<int:type>/', csrf_exempt(viewstest.warningParse), name='warningParse'),
    path('monitor/', monitor.views.index),
    path('insert/', monitor.views.insert_alert),
]

