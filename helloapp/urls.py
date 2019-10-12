# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:30:40 2019

@author: CJP
"""

from django.conf.urls import url
from django.views.generic import RedirectView

from helloapp import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'about/',views.AboutPageView.as_view()),
    url(r'plotly/',views.PlotPageView.as_view()),# Add this /about/ route
    url(r'PageExample/',views.SamplePageView.as_view()),
    url(r'TagExample/',views.TemplatePageView.as_view()),
    url(r'^plotly_movies1/$', RedirectView.as_view(url='https://chart-studio.plot.ly/~chandnijoshi/62.embed'),name='plotly_movies1')
]

#from django.conf.urls import patterns, url
#
#urlpatterns = patterns('',
#    # ...
#
#    url(r'^remote_admin/$', RedirectView.as_view(url='http://admin.mydomain.com'),
#        name='remote_admin'),
#    url(r'^dev_admin/$', RedirectView.as_view(url='http://devadmin.localhost'),
#        name='dev_admin'),
#)