from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.views.generic import RedirectView


urlpatterns = [
    path('polls/', include('polls.urls')),
    path('', RedirectView.as_view(url='/polls/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
