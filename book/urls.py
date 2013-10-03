# coding=utf-8

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('book.views',
    (r'^$', 'index'),
    (r'^index/$', 'index'),
    
    (r'^book/$', 'book'),
    (r'^read_book/$', 'read_book'),
    (r'^delete_book/$', 'delete_book'),
    (r'^update_book/$', 'update_book'),
    (r'^create_book/$', 'create_book'),
    
    (r'^author/$', 'author'),
    (r'^read_author/$', 'read_author'),
    (r'^delete_author/$', 'delete_author'),
    (r'^update_author/$', 'update_author'),
    (r'^create_author/$', 'create_author'),
    #(r'^get_authorlist/$', 'get_authorlist'),
    
    
    (r'^publisher/$', 'publisher'),
    (r'^read_publisher/$', 'read_publisher'),
    (r'^delete_publisher/$', 'delete_publisher'),
    (r'^update_publisher/$', 'update_publisher'),
    (r'^create_publisher/$', 'create_publisher'),
)