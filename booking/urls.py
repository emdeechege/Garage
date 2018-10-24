from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^home/$', views.home, name='home'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^editprofile/$', views.edit_profile, name='edit_profile'),
    url(r'^upload/', views.update_vehicle, name='upload'),
    url(r'^booking/(?P<pk>\d+)', views.add_booking, name='booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
