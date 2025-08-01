from django.contrib import admin
from django.urls import path, include
from . import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/posts/', include('posts.urls')),
    path('api/v1/user/', include('user.urls')),

]

urlpatterns += swagger.urlpatterns
