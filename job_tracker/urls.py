from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit', views.edit_profile, name='edit_profile'),
    path('accounts/index/', views.index, name='index'),
    path('applications/', views.application, name='application')
    path('contacts/create', views.ContactCreate.as_view(), name='contacts_create'),
    path('contacts/update', views.ContactUpdate.as_view(), name='contacts_update'),
    path('contacts/delete', views.ContactDelete.as_view(), name='contacts_delete'),
    path('landmarks/', views.LandmarkList.as_view(),
    name='landmarks_index'),
    path('landmarks/<int:pk>/', views.LandmarkDetail.as_view(), name='landmarks_detail'),
    path('landmarks/create', views.LandmarkCreate.as_view(), name='landmarks_create'),
    path('landmarks/<int:pk>/update', views.LandmarkUpdate.as_view(), name='landmarks_update'),
    path('landmarks/<int:pk>/delete', views.Landmark_delete.as_view(), name='landmarks_delete'),
    path('landmarks/<int:landmark_id>/assoc_app/<int:application_id>/', views.assoc_landmark, name='assoc_landmark'),
]
