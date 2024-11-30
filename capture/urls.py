from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # For rendering the capture page
    path('upload/', views.upload_image, name='upload_image'),  # For handling image uploads
    path('login/', views.login_view, name='login'),
]
