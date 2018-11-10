from datetime import datetime, date, timedelta
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import render_to_response, get_object_or_404
from models import Issue, Article, Author
from django.db.models import Q 
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed


def latest_articles():
    entries = Article.objects.filter(published=True).order_by('-issue__publish_date')
    return entries

class LatestEntriesFeed(Feed):
    title = "Hypocrite Reader"
    link = "/"
    description = "An online monthly, of essays conceptual and timely, based in Brooklyn, New York."

    def items(self):
        return latest_articles()[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

def latest_issue():
    cutoff_date = datetime.now()
    list = Issue.objects.filter(published=True, publish_date__lte=cutoff_date).order_by('-publish_date')
    if list.count() > 0:
        latest_issue = list[0]
        return latest_issue
    else:
        return None

def issue_detail(request, issue_number):
    cutoff_date = datetime.now()
    issue = get_object_or_404(Issue,issue_number=issue_number,published=True, publish_date__lte=cutoff_date)
    articles = issue.contents()
    afterthoughts = issue.afterthoughts()
    context = {
        'issue': issue,
        'articles': articles,
        'afterthoughts': afterthoughts,
    }
    return render_to_response("myapp/issue.html", context,
                              context_instance=RequestContext(request))

def front_page(request):
    issue = latest_issue()
    if issue is None:
        return render_to_response("myapp/issue.html", {},
                              context_instance=RequestContext(request))
    else:
        return issue_detail(request,issue.issue_number)

def about(request):
    issue = latest_issue()
    context = {
        'issue': issue,
    }
    return render_to_response("myapp/about.html", context,
                              context_instance=RequestContext(request))

def contribute(request):
    issue = latest_issue()
    context = {
        'issue': issue,
    }
    return render_to_response("myapp/contribute.html", context,
                              context_instance=RequestContext(request))

def anthology(request):
    issue = latest_issue()
    context = {
        'issue': issue,
    }
    return render_to_response("myapp/anthology.html", context,
                              context_instance=RequestContext(request))

def archive(request):
    issues = Issue.objects.filter(published=True).order_by('-publish_date')
    context = {
        'issues': issues,
    }
    return render_to_response("myapp/archive.html", context,
                              context_instance=RequestContext(request))

def author(request,author_slug):
    author = get_object_or_404(Author,slug=author_slug)
    articles = author.articles_by()
    articles_illustrated = author.articles_illustrated_by()
    context = {
        'author': author,
        'articles': articles,
        'articles_illustrated': articles_illustrated,
    }
    return render_to_response("myapp/author.html", context,
                              context_instance=RequestContext(request))

def article_detail(request, issue_number, article_slug):
    issue = get_object_or_404(Issue,issue_number=issue_number)
    article = get_object_or_404(Article,slug=article_slug,published=True)
    context = {
        'issue': issue,
        'article': article,
        'afterthoughts_for': article.afterthoughts_for(),
    }
    return render_to_response("myapp/article.html", context,
                              context_instance=RequestContext(request))
def article_detail_comments(request, issue_number, article_slug):
    issue = get_object_or_404(Issue,issue_number=issue_number)
    article = get_object_or_404(Article,slug=article_slug,published=True)
    context = {
        'issue': issue,
        'article': article,
        'afterthoughts_for': article.afterthoughts_for(),
    }
    return render_to_response("myapp/article_comments.html", context,
                              context_instance=RequestContext(request))

def article_detail_print(request, issue_number, article_slug):
    issue = get_object_or_404(Issue,issue_number=issue_number)
    article = get_object_or_404(Article,slug=article_slug)
    context = {
        'issue': issue,
        'article': article,
    }
    return render_to_response("myapp/article_print.html", context,
                              context_instance=RequestContext(request))
