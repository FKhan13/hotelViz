from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^(?P<country>\D+)/selection/$', views.selection, name='selection'),
    url(r'^(?P<country>\D+)/bar$', views.field, name='bar'),
    url(r'^(?P<country>\D+)/motion$', views.motion, name='motion'),

    # (?P<fields>.+)
]
