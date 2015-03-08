from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from oscar.app import application
from oscar.views import handler500, handler404, handler403

from apps.custom.sitemaps import base_sitemaps
# from apps.custom.api import *
# from apps.test_shibboleth import views

from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Include admin as convenience. It's unsupported and you should
    # use the dashboard
    url(r'^admin/', include(admin.site.urls)),

    # API module
    url(r'^api/', include('apps.custom.api.urls')),

    # Library doesn't have any view
    # url(r'^library/', include('apps.custom.library.urls')),

    # Mepin secure payments API
    # url(r'^mepin/', include('apps.mepin.urls')),

    # i18n URLS need to live outside of i18n_patterns scope of the shop
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Basic sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {
        'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap', {'sitemaps': base_sitemaps}),


    # AJAX
    url(r'^ajax/$', 'apps.custom.ajax.home.loadItems'),

    # OAuth2 integration
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),

    # Use swagger to show the API
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r"^/", RedirectView.as_view(url='/catalogue/')),
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns('',
                             url(r'^info/', include('apps.custom.info.urls')),
                             url(r'^panel/', include('apps.custom.panel.urls')),

                             # Custom functionality to allow dashboard users to be created
                             # url(r'gateway/', include('apps.gateway.urls')),

                             # Oscar's normal URLs
                             url(r'', include(application.urls)),
)
# Shibboleth
urlpatterns += patterns('',
                        url(r'^shib/', include('apps.contrib.customer.urls', namespace='shibboleth')),
)

if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        url(r'^403$', handler403),
        url(r'^404$', handler404),
        url(r'^500$', handler500),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    # test_shibboleth attributes
    urlpatterns += patterns('',
                            # url(r'^shibboleth/login', 'apps.test_shibboleth.views.foo'),
    )