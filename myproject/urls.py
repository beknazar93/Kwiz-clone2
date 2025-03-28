from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def auth_redirect(request):
    return redirect('/login/auth0/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', auth_redirect, name='auth_redirect'),
    path('', include('social_django.urls', namespace='social')),
]
