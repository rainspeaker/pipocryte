from django.conf.urls.defaults import patterns, include, url
from myapp.views import issue_detail, article_detail, about, anthology, latest_issue, contribute, archive, author, front_page, article_detail_print, LatestEntriesFeed, article_detail_comments
from myapp.models import Issue, Author, Article
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',front_page, name='front-page'),
    url(r'^admin_site/', include(admin.site.urls)),
    url('^contributor/(?P<author_slug>[a-z0-9_-]+)/$', author, name='author-page'),
    url('^about(?:\.html/)?', about, name='about'),
    url('^contribute(?:\.html/)?', contribute, name='contribute'),
    url('^anthology(?:\.html/)?', anthology, name='anthology'),
    url('^archive(?:\.html|/)?$', archive, name='archive'),
    url('^(?P<issue_number>[0-9]+)/(index\.html)?$', issue_detail, name='issue-contents'),
    url('^(?P<issue_number>[0-9]+)/(?P<article_slug>[a-z0-9_-]+)(\.html|/)?$', article_detail, name='article-detail'),
    url('^comments/(?P<issue_number>[0-9]+)/(?P<article_slug>[a-z0-9_-]+)(\.html|/)?$', article_detail_comments, name='article-detail-comments'),
    url('^(?P<issue_number>[0-9]+)/(?P<article_slug>[a-z0-9_-]+)(\.html|/)?/print$', article_detail_print, name='article-detail-print'),
    url('^feed/$', LatestEntriesFeed(), name='latest-feed'),
)
