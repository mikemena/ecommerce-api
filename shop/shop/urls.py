"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import include, path
import store.views

# The path() function is passed four arguments, two required: route and view

urlpatterns = [
    path("store/", include("store.urls")),
    path("admin/", admin.site.urls),
    path("products/<int:id>/", store.views.show, name="show-product"),
    path("cart/", store.views.cart, name="shopping-cart"),
    path("", store.views.index, name="list-products"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
