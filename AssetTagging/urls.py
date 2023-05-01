from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('admin/', include('backend.urls', namespace='backend')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


