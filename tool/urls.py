#encoding:utf-8

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^$', 'tool.views.index'),
  (r'^calenda_maker/', 'tool.views.calenda_maker'),
)

