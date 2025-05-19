"""
URL configuration for wallet_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from wallet_app import views as wallet_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1) login at "/"
    path(
        '',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    # 2) logout goes back to login
    # path(
    #     'logout/',
    #     auth_views.LogoutView.as_view(next_page='login'),
    #     name='logout'
    # ),
    path('logout/', wallet_views.logout_view, name='logout'),

    # 3) registration
    path('register/', wallet_views.register_view, name='register'),

    # 4) wallet app pages (deposit/, withdraw/, etc.)
    path('', include('wallet_app.urls')),
]
schema_view = get_schema_view(
   openapi.Info(
      title="Wallet Admin API",
      default_version='v1',
      description="APIs for flagged transactions, balances, and top users",
   ),
   public=False,
   permission_classes=[permissions.IsAdminUser],
)

urlpatterns += [
    path('api/', include('wallet_app.api.urls')),  # /api/flags/, /api/balances/, /api/top-users/
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]