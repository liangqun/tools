#encoding:utf-8
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#import blog.urls

urlpatterns = patterns('',
    (r'^$', 'tool.views.index'),
    # (r'^$',lambda x:HttpResponseRedirect('/blog/')),
    # (r'^admin/', include(admin.site.urls)),
    (r'^tool/', include('tool.urls')),
)