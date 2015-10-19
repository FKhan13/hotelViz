from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^explore/', views.ExploreView.as_view(), name='explore'),
    url(r'set/', views.SetView.as_view(), name='set'),
    url(r'expenditure/', views.Expenditure.as_view(), name='expenditure'),
    url(r'^(?P<country>\D+)/selection/$', views.selection, name='selection'),
    url(r'^(?P<country>\D+)/bar$', views.field, name='bar'),
    url(r'^(?P<country>\D+)/motion$', views.motion, name='motion'),
    url(r'^play/', views.play, name='play'),
    url(r'^week_selection/', views.week_selection, name='week_selection'),

    # (?P<fields>.+)
]
