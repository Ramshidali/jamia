from . import views
from django.urls import path, re_path

# Create your tests here.

app_name = 'institution'

urlpatterns = [
    path('institution/', views.institution_list, name='institution_list'),
    re_path(r'^institution/(?P<pk>.*)/$', views.institution, name='institution'),
    re_path(r'^create-institution/$', views.create_institution, name='create_institution'),
    re_path(r'^edit-institution/(?P<pk>.*)/$', views.edit_institution, name='edit_institution'),
    re_path(r'^delete-institution/(?P<pk>.*)/$', views.delete_institution, name='delete_institution'),

    re_path(r'^institution_facility/(?P<pk>.*)/$', views.institution_facility_single, name='institution_facility'),
    re_path(r'^institution_facilities/(?P<institution_pk>.*)/$', views.institution_facilities, name='institution_facilities'),
    re_path(r'^create-institution-facility/$', views.create_institution_facility, name='create_institution_facility'),
    re_path(r'^edit-institution-facility/(?P<pk>.*)/$', views.edit_institution_facility, name='edit_institution_facility'),
    re_path(r'^delete-institution-facility/(?P<pk>.*)/$', views.delete_institution_facility, name='delete_institution_facility'),

    re_path(r'^institution_about/(?P<pk>.*)/$', views.institution_about_single, name='institution_about'),
    re_path(r'^create-institution-about/$', views.create_institution_about, name='create_institution_about'),
    re_path(r'^edit-institution-about/(?P<pk>.*)/$', views.edit_institution_about, name='edit_institution_about'),
    re_path(r'^delete-institution-about/(?P<pk>.*)/$', views.delete_institution_about, name='delete_institution_about'),

    re_path(r'^institution-testimonial/(?P<pk>.*)/$', views.institution_testimonial_single, name='institution_testimonial'),
    re_path(r'^institution-testimonial-list/(?P<institution_pk>.*)/$', views.institution_testimonials, name='institution_testimonials'),
    re_path(r'^create-institution-testimonial/$', views.create_institution_testimonial, name='create_institution_testimonial'),
    re_path(r'^edit-institution-testimonial/(?P<pk>.*)/$', views.edit_institution_testimonial, name='edit_institution_testimonial'),
    re_path(r'^delete-institution-testimonial/(?P<pk>.*)/$', views.delete_institution_testimonial, name='delete_institution_testimonial'),

    re_path(r'^institution-department/(?P<pk>.*)/$', views.institution_department_single, name='institution_department'),
    re_path(r'^institution-department-list/(?P<institution_pk>.*)/$', views.institution_departments, name='institution_departments'),
    re_path(r'^create-institution-department/$', views.create_institution_department, name='create_institution_department'),
    re_path(r'^edit-institution-department/(?P<pk>.*)/$', views.edit_institution_department, name='edit_institution_department'),
    re_path(r'^delete-institution-department/(?P<pk>.*)/$', views.delete_institution_department, name='delete_institution_department'),

    re_path(r'^institution-galleries/(?P<institution_pk>.*)/$', views.institution_gallery_list, name='gallery_list'),
    re_path(r'^create-institution-gallery/$', views.create_institution_gallery, name='create_institution_gallery'),
    re_path(r'^delete-institution-gallery/(?P<pk>.*)/$', views.delete_institution_gallery, name='delete_institution_gallery'),

    re_path(r'^create-institution-management-team/(?P<pk>.*)/$', views.create_institution_management_team, name='create_institution_management_team'),
    re_path(r'^edit-institution-management-team/(?P<pk>.*)/$', views.edit_institution_management_team, name='edit_institution_management_team'),
    re_path(r'^delete-institution-management-team/(?P<pk>.*)/$', views.delete_institution_management_team, name='delete_institution_management_team'),

    re_path(r'^institution-contact/(?P<pk>.*)/$', views.institution_contact_single, name='institution_contact'),
    re_path(r'^create-institution-contact/$', views.create_institution_contact, name='create_institution_contact'),
    re_path(r'^edit-institution-contact/(?P<pk>.*)/$', views.edit_institution_contact, name='edit_institution_contact'),
    re_path(r'^delete-institution-contact/(?P<pk>.*)/$', views.delete_institution_contact, name='delete_institution_contact'),

    re_path(r'^create-department-faculty/(?P<pk>.*)/$', views.create_department_faculty, name='create_department_faculty'),
    re_path(r'^edit-department-faculty/(?P<pk>.*)/$', views.edit_department_faculty, name='edit_department_faculty'),
    re_path(r'^delete-department-faculty/(?P<pk>.*)/$', views.delete_department_faculty, name='delete_department_faculty'),

    re_path(r'^create-department-service/(?P<pk>.*)/$', views.create_department_services, name='create_department_services'),
    re_path(r'^edit-department-service/(?P<pk>.*)/$', views.edit_department_services, name='edit_department_services'),
    re_path(r'^delete-department-service/(?P<pk>.*)/$', views.delete_department_services, name='delete_department_services'),

    re_path(r'^create-event/$', views.create_institute_events, name='create_institute_events'),
    re_path(r'^edit-event/(?P<pk>.*)/$', views.edit_institute_events, name='edit_institute_events'),
    re_path(r'^delete-event/(?P<pk>.*)/$', views.delete_institute_events, name='delete_institute_events'),

]