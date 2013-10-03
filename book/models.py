# coding=utf-8

from django.db import models
from datetime import datetime

class Publisher(models.Model):
    '''
    @note: 出版社
    '''
    #id  django自动生成的primary_key
    name     = models.CharField(u'出版社', max_length=30, blank=False)
    address  = models.CharField(u'地址', max_length=50, blank=False)
    city     = models.CharField(u'城市', max_length=30, blank=False)
    province = models.CharField(u'省份', max_length=30, blank=False)
    country  = models.CharField(u'国家', max_length=50, blank=False)
    website  = models.URLField(u'网址', null=True)
    
    def __unicode__(self):
        return self.name
    
class Author(models.Model):
    '''
    @note: 作者
    '''
    name  = models.CharField(u'姓名', max_length=40, blank=False) #不可为空
    email = models.EmailField(u'邮件', null=True, blank=True)     #可以为空
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class Book(models.Model):
    '''
    @note: 书籍
    '''
    title            = models.CharField(u'书名', max_length=128)
    authors          = models.ManyToManyField(Author, verbose_name=u'作者')
    publisher        = models.ForeignKey(Publisher, verbose_name=u'出版商')
    publication_date = models.DateTimeField(u'出版日期', default=datetime.now())
    price            = models.IntegerField(u'价格', default=0)
    
    def __unicode__(self):
        return self.title
    
