from django.contrib import admin
from django.urls import path, include

from annonces_esp import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentification.urls')),  
    path('', include('acceuil.urls')),  
    path('dashboard/', include('Dashboard.urls')),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)