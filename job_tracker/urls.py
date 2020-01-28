from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/index/', views.index, name='index'),
    path('applications/', views.application, name='application'),
    path('applications/<int:application_id>/', views.applications_detail, name='applications_detail'),
    path('applications/create/', views.ApplicationCreate.as_view(), name='applications_create'),
    path('applications/<int:pk>/update/', views.ApplicationUpdate.as_view(), name='applications_update'),
    path('applications/<int:pk>/delete/', views.ApplicationDelete.as_view(), name='applications_delete'),
    path('contacts/index/', views.contacts_index, name='contacts_index'),
    path('applications/<int:application_id>/add_landmarks/', views.add_landmark, name='add_landmark'),
    path('contacts/<int:contact_id>/', views.contacts_detail, name='contacts_detail'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contacts_create'),
    path('contacts/<int:pk>/update/', views.ContactUpdate.as_view(), name='contacts_update'),
    path('contacts/<int:pk>/delete/', views.ContactDelete.as_view(), name='contacts_delete'),
    path('landmarks/<int:pk>/update/', views.LandmarkUpdate.as_view(), name='landmarks_update'),
    path('landmarks/<int:pk>/delete/', views.LandmarkDelete.as_view(), name='landmarks_delete'),
    path('landmarks/<int:landmark_id>/assoc_app/<int:application_id>/', views.assoc_landmark, name='assoc_landmark'),
    path('ajax/jobsearch/', views.job_search, name='job_search'),
    path('ajax/job_search_api/', views.job_search_api, name='job_search_api'),
    path('ajax/get_calendar/', views.get_calendar, name='get_calendar'),
    path('calendar/', views.calendar, name='calendar'),
  ]