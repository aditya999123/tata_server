"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from add_user.views import add_user_fun,login,change_password
from users.views import view_users,view_profile
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_user/', add_user_fun),
    url(r'^login/', login),
    url(r'^change_password/', change_password),
    url(r'^view_user/', view_users),
    url(r'^profile/', view_profile),
#    url(r'^dealer/', dealer),
]
admin.site.site_header = "TATA Administration"#"Code Nicely's Administration"
admin.site.index_title = 'TataMotors'
admin.site.site_title = 'NIT Raipur'

from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
