"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', include("hw.urls")), # the main website url (going to hw right now)
    path('admin/', admin.site.urls),
    path('hw/', include("hw.urls")), # we create the URL hw/, and associate it with the URLs in another file
    path('quotes/', include("quotes.urls")), # assignment 3
    path('formdata/', include("formdata.urls")), # class 9/24
    path('restaurant/', include("restaurant.urls")), # assignment 4
    path('blog/', include("blog.urls")), # class 10/1
    path('mini_fb/', include("mini_fb.urls")), # assignment 5
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # creating a list anc concatenating one more thing
