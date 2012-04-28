#encoding:utf-8

from django.conf.urls.defaults import patterns
from tool import views

urlpatterns = patterns('',
  (r'^$', views.index),
  (r'^calenda_maker/', views.calenda_maker),
)

