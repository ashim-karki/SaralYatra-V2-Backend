from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls", namespace="auth")),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
