# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import  render_to_response
from book.models import Book,Author,Publisher

import json
import datetime

def index(request):
    '''
    @note: 首页
    '''
    return render_to_response("book/index.html", {})

def book(request):
    '''
    @note: 图书管理
    '''
    operation = request.POST.get("operation")
    
    if operation == "create":
        return create_author(request)
    if operation == "destroy":
        return delete_author(request)
    if operation == "update":
        return update_author(request)
    
    authorlist    = []
    publisherlist = []
    try:
        authors = Author.objects.all() #获取数据
        for author in authors:
            authorlist.append(author.name)
        publishers = Publisher.objects.all()
        for publisher in publishers:
            publisherlist.append(publisher.name)
    except:
        authorlist    = []
        publisherlist = []
    print authorlist
    return render_to_response("book/book.html",{'authorlist': authorlist, 'publisherlist': publisherlist})


def gt(dt_str):
    '''
    @note: 格式化时间
    '''
    dt, _, us= dt_str.partition(".")
    dt= datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us= int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)

def create_book(request):
    '''
    @note: 添加图书信息
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    print models_json
    try:
        datalist = []
        for data in models_json:
            if Book.objects.filter(title=data['title']):
                return HttpResponse(json.dumps({'result':False, 'message': u'书籍 %s 的信息已存在!' % data['title']}))
            else:
                print "create"
                print data['publication_date']
                print data['authors']
                print data['publisher']
                publisher = Publisher.objects.filter(name=data['publisher'])[0]
                print publisher
                book = Book()
                book.title = data['title']
                book.publication_date = gt(data['publication_date'])
                book.publisher = publisher
                book.price = data['price']
                book.save()
                #解析authors并添加
                authors = data['authors'].split(',')
                authorlist = []
                for name in authors:
                    authorlist.append(Author.objects.filter(name=name)[0])
                print authorlist
                for author in authorlist:
                    book.authors.add(author)
                datalist.append(data)
    except Exception, e:
        print e
        return HttpResponse(json.dumps({'result':False, 'message': u'添加记录失败, %s' % e}))
    return HttpResponse(json.dumps({'result':True, 'data': datalist}))
        
def read_book(request):
    '''
    @note: 读取图书信息
    '''
    #当前页码
    page     = int(request.GET.get('page', ''))
    #每页记录数
    pagesize = int(request.GET.get('pageSize', ''))
    #分片起始位置
    start = (page - 1) * pagesize
    #分片结束位置
    end   = start + pagesize
    datalist = []
    try:
        booklist = Book.objects.all().order_by('title')
        total    = booklist.count()
        for book in booklist[start:end]:
            #获取书籍所对应的作者(可能含有多个作者)
            authorlist = book.authors.all()
            authors = ""
            for author in authorlist:
                authors += author.name + ","
            datalist.append({
                    'id':               book.pk,
                    'title':            book.title,
                    'publisher':        book.publisher.name,
                    'authors':          authors,
                    'publication_date': str(book.publication_date),
                    'price':            book.price
            })
    except Exception, e:
        return HttpResponse(json.dumps({'result':False, 'message': u"读取记录失败, %s" % e}))
    
    #返回json串
    print datalist
    return HttpResponse(json.dumps({'data':datalist, 'total':total}))
    


def update_book(request):
    '''
    @note: 更新图书信息
    '''  
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    datalist = []
    try:
        for data in models_json:
            print "update"
            print data['publisher']
            publisher = Publisher.objects.filter(name=data['publisher'])[0]
            book = Book.objects.filter(pk=data['id']).update(
                                                title = data['title'],
                                                publication_date = gt(data['publication_date']),
                                                price = data['price'],
                                                publisher = publisher
                                            )
#            publisher = Publisher.objects.filter(name=data['publisher'])[0]
#            book.title            = data['title']
#            book.publication_date = gt(data['publication_date'])
#            book.price            = data['price']
            #更新出版社信息(外键)
            #book.save()
           # book.pulisher = publisher
            
            print book.publisher
            #更新作者信息，先remove原来的作者，再add新作者
            old_authorlist = book.authors.all()
            for author in old_authorlist:
                book.authors.remove(author)
            authors = data['authors'].split(',')
            print authors
            print "update"
            for name in authors:
                print "in"
                author = Author.objects.filter(name=name)[0]
                print author
                if author:
                    book.authors.add(author)
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'更新记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))
    

def delete_book(request):
    '''
    @note: 删除图书信息
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    
    datalist = []
    try:
        for data in models_json:
            pk = data['id']
            Book.objects.filter(pk=pk).delete()
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'删除记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))
  
def author(request):
    '''
    @note: 作者管理，后台分页
    '''
    operation = request.POST.get("operation")
    print "read"
    if operation == "create":
        return create_author(request)
    if operation == "destroy":
        return delete_author(request)
    if operation == "update":
        return update_author(request)        
    
    authorlist = []
    try:
        authors = Author.objects.all()
        for author in authors:
            authorlist.append(author.name)
    except:
        authorlist = []
    print authorlist
    return render_to_response("book/author.html",{'authorlist': authorlist})
    
def create_author(request):
    '''
    @note: 增加作者
    '''
    models=request.POST.get('models','{}')
    models_json = json.loads(models)
    datalist = []
    try:
        for data in models_json:
            author = Author.objects.create(
                            name = data['name'],
                            email = data['email']
                    )
            data['id'] = author.pk
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False, 'message': u'添加记录失败,%e' % e}))
    return HttpResponse(json.dumps({'result':True, 'data': datalist}))

def read_author(request):
    '''
    @note: authors后台分页
    '''
    #当前页码
    page     = int(request.GET.get('page', ''))
    #每页记录数
    pagesize = int(request.GET.get('pageSize', ''))
    #分片起始位置
    start = (page - 1) * pagesize
    #分片结束位置
    end   = start + pagesize
    datalist = []
    try:
        authorlist = Author.objects.all()
        total      = authorlist.count()
        for author in authorlist[start:end]:
            datalist.append({
                    'id':    author.pk,
                    'name':  author.name,
                    'email': author.email,
            })
    except Exception, e:
        return HttpResponse(json.dumps({'result':False, 'message': u"读取记录失败, %s" % e}))
    
    #返回json串
    print datalist
    return HttpResponse(json.dumps({'data':datalist, 'total':total}))

def update_author(request):
    '''
    @note: 更新作者
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    datalist = []
    try:
        for data in models_json:
            Author.objects.filter(pk=data['id']).update(
                                                name = data['name'],
                                                email = data['email']
                                                )
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'更新记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))
     

def delete_author(request):
    '''
    @note: 删除作者
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    
    datalist = []
    try:
        for data in models_json:
            pk = data['id']
            Author.objects.filter(pk=pk).delete()
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'删除记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))
    
def get_authorlist(request):
    '''
    @note: 获取作者名单
    '''
    authorlist = []
    try:
        authors = Author.objects.all()
        for author in authors:
            authorlist.append({'name': author.name})
    except Exception, e:
        pass
    print authorlist
    return HttpResponse(json.dumps(authorlist))

def publisher(request):
    '''
    @note: 出版社管理
    '''
    return render_to_response("book/publisher.html", {})

def create_publisher(request):
    '''
    @note: 添加出版社
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    print models_json
    try:
        datalist = []
        for data in models_json:
            if Publisher.objects.filter(name=data['name']):
                return HttpResponse(json.dumps({'result':False, 'message': u'出版社 %s 已存在' % data['name']}))
            else:
                print "create"
                Publisher.objects.create(
                                    name = data['name'],
                                    address = data['address'],
                                    city = data['city'],
                                    province = data['province'],
                                    country = data['country'],
                                    website = data['website']
                                    )
    except Exception, e:
        return HttpResponse(json.dumps({'result':False, 'message': u'添加记录失败, %s' % e}))
    return HttpResponse(json.dumps({'result':True, 'data':datalist}))

def read_publisher(request):
    '''
    @note: 读取出版社信息
    '''
    page = int(request.GET.get('page', ''))
    pagesize = int(request.GET.get('pageSize'))
    
    start = (page - 1)*pagesize
    end   = start + pagesize
    
    datalist = []
    try:
        publisherlist = Publisher.objects.all()
        total = publisherlist.count()
        for publisher in publisherlist[start:end]:
            datalist.append({
                        'id': publisher.pk,    
                        'name': publisher.name,
                        'address': publisher.address,
                        'city':  publisher.city,
                        'province': publisher.province,
                        'country': publisher.country,
                        'website': publisher.website
                        })
    except Exception, e:
        return HttpResponse(json.dumps({'result':False, 'message': u'读取信息失败, %s' % e}))
    print datalist
    return HttpResponse(json.dumps({'data':datalist, 'total': total}))
    
def update_publisher(request):
    '''
    @note: 更新出版社信息
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    datalist = []
    try:
        for data in models_json:
            Publisher.objects.filter(pk=data['id']).update(
                                                name = data['name'],
                                                address = data['address'],
                                                city    = data['city'],
                                                province  = data['province'],
                                                country   = data['country'],
                                                website   = data['website']                                                
                                                )
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'更新记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))  
    
def delete_publisher(request):
    '''
    @note: 删除出版社
    '''
    models = request.POST.get('models', '{}')
    models_json = json.loads(models)
    
    datalist = []
    try:
        for data in models_json:
            pk = data['id']
            Publisher.objects.filter(pk=pk).delete()
            datalist.append(data)
    except Exception, e:
        return HttpResponse(json.dumps({'result':False,'message':u'删除记录失败，%s' % e}))
    return HttpResponse(json.dumps({'result':True,'data': datalist}))