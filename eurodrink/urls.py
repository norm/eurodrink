from django.conf.urls import include, url
from django.contrib import admin

from homepage.views import HomepageView
urlpatterns = [
    # Examples:
    # url(r'^$', 'eurodrink.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomepageView.as_view()),
]
