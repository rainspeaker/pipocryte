from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models import permalink


class Issue(models.Model):
    """The Issue class
    """
    title = models.CharField(max_length=400)
    issue_number = models.IntegerField(unique=True)
    slug = models.CharField(max_length=100, unique=True)
    published = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=datetime.now)
    rendered_about = models.TextField(blank=True, null=True)
    rendered_contribute = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def contents(self):
        entries = Article.objects.filter(issue = self, afterthoughts = False, published=True).order_by('ordinal')
        return entries

    def contents_all(self):
        entries = Article.objects.filter(issue = self,published=True).order_by('ordinal')
        return entries

    def afterthoughts(self):
        entries = Article.objects.filter(issue = self, afterthoughts = True, published=True).order_by('ordinal')
        return entries

    @permalink
    def get_absolute_url(self):
        return ('issue-contents', (self.issue_number,))

class Author(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.CharField(max_length=1000,blank=True, null=True)
    slug = models.CharField(max_length=40, unique=True)
    page_url = models.URLField(max_length=1000,blank=True, null=True)
    page_name = models.CharField(max_length=400,blank=True, null=True)
    twitter_name = models.CharField(max_length=50,blank=True, null=True)

    def __unicode__(self):
        return self.name()

    @permalink
    def get_absolute_url(self):
        return ('author-page',(self.slug,))

    def name(self):
        return "%s %s" % (self.firstname,self.lastname)

    def articles_by_unpublished_included(self):
        entries = Article.objects.filter(authors = self).order_by('-issue__publish_date')
        return entries

    def articles_by(self):
        entries = Article.objects.filter(authors = self,published=True).order_by('-issue__publish_date')
        return entries

    def articles_illustrated_by(self):
        entries = Article.objects.filter(illustrators = self,published=True).order_by('-issue__publish_date')
        return entries


class Article(models.Model):
    title = models.CharField(max_length=400)

    author = models.ForeignKey(Author, blank=True, null=True)
    authors = models.ManyToManyField(Author, blank=True, null=True, related_name="article-authors")
    illustrators = models.ManyToManyField(Author, blank=True, null=True, related_name="article-illustrator")
    issue = models.ForeignKey(Issue, blank=True, null=True, related_name="article-issue")
    ordinal = models.IntegerField(blank=True, null=True)

    afterthoughts = models.BooleanField(default=False)
    afterthoughts_article = models.ForeignKey('self',blank=True,null=True)
    afterthoughts_issue = models.ForeignKey(Issue,blank=True,null=True, related_name="article-afterthoughts-issue")

    slug = models.CharField(max_length=100, unique=True)

    rendered_content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    search_keywords = models.TextField(blank=True,null=True)

    creation_date = models.DateTimeField(default=datetime.now)
    published = models.BooleanField(default=False)
    hascomments = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def publish_date(self):
        return issue.publish_date

    @permalink
    def get_absolute_url(self):
        return ('article-detail', (self.issue.issue_number,self.slug))

    def afterthoughts_for(self):
        list = Article.objects.filter(afterthoughts_article=self,published=True,)
        return list
