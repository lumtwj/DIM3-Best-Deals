from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'DIM.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       #regular expression to detect bestbuy with/
                       #created 2 type of ways to do html pages
                       url(r'^$', 'BestBuy.views.index', name='home'),
                       url(r'^bestbuy/auth/$', 'BestBuy.views.auth_view'),
                       url(r'^bestbuy/logout/$', 'BestBuy.views.logout'),
                       url(r'^bestbuy/relogin/$', 'BestBuy.views.relogin'),
                       url(r'^bestbuy/register/$', 'BestBuy.views.register'),
                       url(r'^bestbuy/register_sucess/$', 'BestBuy.views.register_sucess'),
                       url(r'^bestbuy/searchperf/$', 'BestBuy.views.searchistory'),
                       url(r'^bestbuy/search/$', 'BestBuy.views.search'),
                       url(r'^bestbuy/addfav/$', 'BestBuy.views.addfavourite'),
                       url(r'^bestbuy/editprofile/$', 'BestBuy.views.editprofile'),
                       url(r'^bestbuy/favourite/$', 'BestBuy.views.favourite'),
                       url(r'^bestbuy/index/$', 'BestBuy.views.index'),
                       url(r'^bestbuy/deletefav/$', 'BestBuy.views.deletefav'),
                        url(r'^bestbuy/about/$', 'BestBuy.views.about'),
                       #  url(r'^bestbuy/search/$', 'BestBuy.views.search'),
                       url(r'admin/', include(admin.site.urls)),
                       )
