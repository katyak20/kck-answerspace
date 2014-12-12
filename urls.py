
from django.conf.urls.defaults import patterns, include, url
from answerspace.views import pupils
from django.contrib import admin

admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
(r'^pupils/$', graphs),
(r'^machines/$', machines),
(r'^admin/', include(admin.site.urls)),
#(r'^statsForOneMachine/$', 'monitor.views.statsForOneMachine'),

# Examples:
# url(r'^$', 'monitor.views.home', name='home'),
# url(r'^monitor/', include('monitor.foo.urls')),
# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
)