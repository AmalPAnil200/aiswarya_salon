from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index', views.index_view, name='index'),
    path('', views.home_view, name='home'),
    path('pricing', views.pricing_view, name='pricing'),
    path('media', views.media_view, name='media'),\
    path('about_us', views.about_us_view, name='about_us'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
