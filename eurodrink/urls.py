from django.conf.urls import include, url
from django.contrib import admin

from homepage.views import HomepageView
from controlpanel.views import ControlPanelView, TweetView


urlpatterns = [
    # Examples:
    # url(r'^$', 'eurodrink.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'panel/$', ControlPanelView.as_view()),
    url(r'panel/tweet$', TweetView.as_view()),

    url(r'^$', HomepageView.as_view()),
]
