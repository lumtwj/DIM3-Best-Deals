from django.http import HttpResponse
# Create your views here.
from django.db import connection
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
from BestBuy.models import productModel1
from BestBuy.models import favouriteModel
from BestBuy.models import ProdRating
from BestBuy.models import searchHistory
from BestBuy.models import UserProfile
from django.core.context_processors import csrf
from DIM.forms import BestBuyRegistrationForm
from django.shortcuts import RequestContext
from datetime import datetime
from django.utils import formats
from DIM.forms import editProfileForm
import sqlite3
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm



def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/bestbuy/index')
    else:
        return HttpResponseRedirect('/bestbuy/index')
        #https://docs.djangoproject.com/en/dev/ref/models/querysets/

def logout(request):
    type = productModel1.objects.distinct().values('type')
    auth.logout(request)
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c,context_instance=RequestContext(request, {"type": type}))


def register(request):
    type = productModel1.objects.distinct().values('type')
    if request.user.is_authenticated():
        return render_to_response('main.html', {'id': request.user.id},
                                  context_instance=RequestContext(request, {"type": type}))
    else:
        if request.method == 'POST':
            form = BestBuyRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/bestbuy/register_sucess')
        c = {}
        c.update(csrf(request))
        c['form'] = BestBuyRegistrationForm()
        return render_to_response('register.html', c)

def editprofile(request):
    if (request.user.is_authenticated()):
        name = request.user.username
        if request.method=='POST':
            form=editProfileForm(request.POST,instance=request.user.profile)
            if form.is_valid():
                form.save()
            return  HttpResponseRedirect('/bestbuy/index')
        else:

            user =request.user
            profile=user.profile
            form =editProfileForm(instance=profile)
        c = {}
        c.update(csrf(request))
        info = UserProfile.objects.filter(user=request.user.id).get()
        c['form']=editProfileForm(initial={'email':info.email,'first_name':info.first_name, 'last_name':info.last_name,
                                           'handphone':info.handphone,'postalcode':info.postalcode,'address':info.address})
        return render_to_response('editprofile.html',c,context_instance=RequestContext(request, {"username": name}))

def register_sucess(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('register_sucess.html',c)


def index(request):
    type = productModel1.objects.distinct().values('type')
    if request.user.is_authenticated():
        username=request.user.username
        return render_to_response('main.html', {'id': request.user.id},
                                  context_instance=RequestContext(request, {"type": type,"username":username}))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('index.html', c, context_instance=RequestContext(request, {"type": type}))


def search(request):

    getuserproduct = favouriteModel.objects.get
    c = {}
    c.update(csrf(request))
    type = productModel1.objects.distinct().values('type')
    getprice = request.POST.get('price')
    item = request.POST.get('search')
    gettype=request.POST.get('type')
    userid = request.user.id
    getrate = ProdRating.objects.raw('select p.id ,p.productid,AVG(p.rate) as averagerate from BestBuy_prodrating p group by p.productid')
    conn1 = sqlite3.connect('db.sqlite3')
    getdate=formats.date_format(datetime.now(), "SHORT_DATETIME_FORMAT")
    recent = [(request.user.id,item,getdate)]
    if (request.user.is_authenticated()):
        username = request.user.username
        if getprice is not None and getprice != '' and gettype is not None and gettype != '':

            item = productModel1.objects.filter(productname__icontains=item) & productModel1.objects.filter(
                type__exact=gettype) & productModel1.objects.filter(price__lte=getprice).order_by('price') & productModel1.objects.exclude(id__in=favouriteModel.objects.filter(user_id=request.user.id).values_list('productid',flat=True))


            if(item.count() !=0):
                conn1.executemany('INSERT INTO BestBuy_searchhistory (user_id,keyword,date) values (?,?,?) ',recent)
                conn1.commit()
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate,"username":username}))
            else:
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type,"username":username}))

        elif gettype is not None and gettype != '' and item is not None and item !='':

            item = productModel1.objects.filter(productname__icontains=item) & productModel1.objects.filter(
                type__exact=gettype).order_by('price') & productModel1.objects.exclude(id__in=favouriteModel.objects.filter(user_id=request.user.id).values_list('productid',flat=True))

            if(item.count() !=0):
                conn1.executemany('INSERT INTO BestBuy_searchhistory (user_id,keyword,date) values (?,?,?) ',recent)
                conn1.commit()
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate,"username":username}))
            else:
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type,"username":username}))
        elif gettype is not None and gettype != '':

            item = productModel1.objects.filter(type__exact=gettype).order_by('price') \
                   & productModel1.objects.exclude(id__in=favouriteModel.objects.filter(user_id=request.user.id).values_list('productid',flat=True))


            if(item.count() !=0):
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate,"username":username}))
            else:
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type,"getrate":getrate,"username":username}))
        elif item is not None and item !='':
            item = productModel1.objects.filter(productname__icontains=item).order_by('price') & productModel1.objects.exclude(id__in=favouriteModel.objects.all().values_list('productid',flat=True))
            if(item.count() !=0):
                conn1.executemany('INSERT INTO BestBuy_searchhistory (user_id,keyword,date) values (?,?,?) ',recent)
                conn1.commit()

                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate,"username":username}))
            else:
                return render_to_response('main.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type,"username":username}))
        else:
            return render_to_response('main.html', c,
                                      context_instance=RequestContext(request, {"info": "No result Found", "type": type,"username":username}))
    else:
        if getprice is not None and getprice != '' and gettype is not None and gettype != '':
            item = productModel1.objects.filter(productname__icontains=item) & productModel1.objects.filter(
                type__exact=gettype) & productModel1.objects.filter(price__lte=getprice).order_by('price')
            if(item.count !=0):
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate}))
            else:
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type}))
        elif gettype is not None and gettype != '' and item is not None and item !='':
            item = productModel1.objects.filter(productname__icontains=item) & productModel1.objects.filter(
                type__exact=gettype).order_by('price')
            if(item.count !=0):
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate}))
            else:
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type}))
        elif gettype is not None and gettype != '':
            item = productModel1.objects.filter(type__exact=gettype).order_by('price')
            if(item.count !=0):
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate}))
            else:
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type}))
        elif item is not None and item !='':
            item = productModel1.objects.filter(productname__icontains=item).order_by('price')
            if(item.count !=0):
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"item": item, "type": type,"getrate":getrate}))
            else:
                return render_to_response('index.html', c,
                                          context_instance=RequestContext(request, {"info": "No result Found", "type": type}))
        else:
            return render_to_response('index.html', c,
                                      context_instance=RequestContext(request, {"info": "No result Found", "type": type}))

def addfavourite(request):
    if (request.user.is_authenticated()):
        name = request.user.first_name
        c = {}
        c.update(csrf(request))
        type = productModel1.objects.distinct().values('type')
        fav = request.POST.get('itemid')
        userid =request.user.id

        conn1 = sqlite3.connect('db.sqlite3')
        cursor = conn1.execute("SELECT * FROM BestBuy_productModel1 WHERE id=?", (fav,))
        for row in cursor:
            favinsert = [(row[0],row[1], row[2], row[3], row[4], row[5], userid)]

        conn = sqlite3.connect('db.sqlite3')
        z = conn.cursor()
        z.executemany('INSERT INTO BestBuy_favouriteModel (productid,productname,price,website,image,type,user_id) VALUES (?,?,?,?,?,?,?)',
                      favinsert)
        conn.commit()
        return HttpResponseRedirect('/bestbuy/index')
    else:
        return HttpResponseRedirect('/bestbuy/index')

def favourite(request):
    if (request.user.is_authenticated()):
        c = {}
        c.update(csrf(request))
        username=request.user.username
        userid = request.user.id
        getfav = favouriteModel.objects.filter(user_id=userid)
        getrate = ProdRating.objects.raw('select p.id ,p.productid,AVG(p.rate) as averagerate from BestBuy_prodrating p group by p.productid')
        return render_to_response('favourite.html', c, context_instance=RequestContext(request, {"getfav": getfav,"getrate":getrate,"username":username}))
    else:
        return HttpResponseRedirect('/bestbuy/index')

def deletefav(request):
    if (request.user.is_authenticated()):
        chkdelete = request.POST.get('remove')
        userid = request.user.id
        getid=request.POST.get('productid')
        if(chkdelete is not None and chkdelete is not ''):
            c = {}
            c.update(csrf(request))

            conn = sqlite3.connect('db.sqlite3')
            z = conn.cursor()
            z.execute('DELETE FROM BestBuy_favouriteModel where user_id=? and productid=?',(userid,getid,))
            conn.commit()
            conn.close()
            return HttpResponseRedirect('/bestbuy/favourite')
        else :
            rating = request.POST.get('rating')
            conn1 = sqlite3.connect('C:\Users\IanYeo\PycharmProjects\DIM\db.sqlite3')
            insrate = [(getid,rating,userid)]
            cursor = conn1.execute("SELECT * FROM BestBuy_prodrating WHERE productid=? AND user_id_id=?",
                                   (getid,userid,))
            check = len(cursor.fetchall())

            if check < 1:
                conn1.executemany('INSERT INTO BestBuy_prodrating (productid,rate,user_id_id) VALUES (?,?,?)',insrate)
                conn1.commit()
            else:
                updaterate = [(getid,rating,userid,getid,userid)]
                conn1.executemany('UPDATE BestBuy_prodrating SET productid=?,rate=?,user_id_id=? where  productid=? AND user_id_id=?',updaterate)
                conn1.commit()
            return HttpResponseRedirect('/bestbuy/favourite')
    else:
        return HttpResponseRedirect('/bestbuy/index')

def searchistory(request):
    if (request.user.is_authenticated()):
        name = request.user.username
        c = {}
        c.update(csrf(request))
        getsearchhistory= searchHistory.objects.filter(user_id=request.user.id)
        return render_to_response('searchhistory.html', c, context_instance=RequestContext(request, {"getsearchhistory": getsearchhistory,"username":name}))
    else:
        return HttpResponseRedirect('/bestbuy/index')

def about(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('about.html', c, context_instance=RequestContext(request))
