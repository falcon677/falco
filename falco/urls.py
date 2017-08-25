from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'node.views.home', name='home'),
    url(r'^shanxing$', 'node.views.shanxing', name='shanxing'),

    url(r'^admin/', include(admin.site.urls)),
]
