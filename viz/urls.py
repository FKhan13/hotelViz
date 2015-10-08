from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^(?P<country>\D+)/selection/$', views.selection, name='selection'),
    url(r'^(?P<country>\D+)/filter/bar$', views.field, name='filter_bar'),
    url(r'^(?P<country>\D+)/filter/motion$', views.motion, name='filter_motion'),
    url(r'^(?P<country>\D+)/bar/$', views.bar, name='bar'),  # wont need this one

    # (?P<fields>.+)
]
