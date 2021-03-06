"""movienator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView
from app import views

urlpatterns = [
	path('', views.index),
	path('<int:pk>/', views.movie),
    path('<int:pk>.json/', views.movie_json),
    path('random.json', views.random_json),
    path('admin/', admin.site.urls),
    path('favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.png'),
            permanent=False),
        name="favicon"
    )
]
