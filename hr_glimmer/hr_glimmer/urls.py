from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/account_2/', permanent=True)),
    path('admin/', admin.site.urls),
    path('verification/', include('verify_email.urls')),	
    path('account_2/', include('account_2.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in auth URLs
]
