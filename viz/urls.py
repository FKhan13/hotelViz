from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^(?P<country>\D+)/selection/$', views.selection, name='selection'),
    url(r'^(?P<country>\D+)/filter/$', views.field, name='filter'),
    url(r'^(?P<country>\D+)/bar/$', views.bar, name='bar'),  # wont need this one

    # (?P<fields>.+)
]
