"""convosight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

# admin.site.site_header = 'Convosight'
# admin.site.site_title = 'Convosight'
# admin.site.index_title = 'Convosight administration'
# admin.empty_value_display = '**Empty**'

# for Api documents
schema_view = get_swagger_view(title='Convosight')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/docs/', schema_view, name='api_doc'),
    path('accounts/', include('rest_framework.urls')),
    path('api/v1/movie/', include('convosight.movie.urls')),
    path('api/v1/auth/', include('convosight.accounts.urls')),
    path('api/v1/cinema/', include('convosight.cinema.urls')),
    path('api/v1/booking/', include('convosight.booking.urls')),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
