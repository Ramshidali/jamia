from django.contrib import admin
from django.views.static import serve
from django.urls import include, path, re_path

from main import views as general_views
from jgi import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', general_views.app, name='app'),
    path('app/accounts/', include('registration.backends.default.urls')),

    path('ckeditor', include('ckeditor_uploader.urls')),

    path('',include(('web.urls'),namespace='web')),

    path('main/',include(('main.urls'),namespace='main')),
    path('institution/',include(('institution.urls'),namespace='institution')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
