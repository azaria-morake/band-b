from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-house/', views.add_house, name='add_house'),
    path('edit-house/<int:house_id>/', views.edit_house, name='edit_house'),
    path('delete-house/<int:house_id>/', views.delete_house, name='delete_house'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
]