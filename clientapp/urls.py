
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from users.views import custom_404_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = custom_404_page