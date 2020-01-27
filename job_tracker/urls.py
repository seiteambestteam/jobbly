from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit', views.edit_profile, name='edit_profile'),
    path('users/', views.index, name='index'),
    path('application/', views.application, name='application')
    path('contact/', views.ContactCreate.as_view(), name='contact_create'),
    path('contact/', views.ContactUpdate.as_view(), name='contact_update'),
    path('contact/', views.ContactDelete.as_view(), name='contact_delete'),
    path('landmark/', views.LandmarkList.as_view(),
    name='landmark_index'),
    path('landmark/<int:pk>/', views.LandmarkDetail.as_view(), name='landmark_detail'),
    path('landmark/create', views.LandmarkCreate.as_view(), name='landmark_create'),
    path('landmark/<int:pk>/update', views.LandmarkUpdate.as_view(), name='landmark_update'),
    path('landmark/<int:pk>/delete', views.Landmark_delete.as_view(), name='landmark_delete'),
]