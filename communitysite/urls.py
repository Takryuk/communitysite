"""communitysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blogs/', include('blogs.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from group import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('group/', include('group.urls')),
    path('blog/', include('blogs.urls')),
    path('event/', include('events.urls')),
    path('message/', include('message.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('group:group_list'), permanent=False))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 追加