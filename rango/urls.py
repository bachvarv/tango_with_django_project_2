'''
Created on 26.06.2017

@author: Vladislav
'''
from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('', 
                       url(r'^$', views.index, name="index"))