from django.contrib import admin
from django.urls import path, include
import add_business_listing.urls
from django.conf import settings
from django.conf.urls.static import static
import display_businesses.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_listing/', include(add_business_listing.urls)),
    path('', include(display_businesses.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
