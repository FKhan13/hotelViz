from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^selection/', views.selection, name='selection'),
    url(r'^(?P<fields>.+)/bar/$', views.bar, name='bar'),
]
