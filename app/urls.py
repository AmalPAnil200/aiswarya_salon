from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home', views.home_view, name='home'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
