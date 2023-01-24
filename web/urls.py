from . import views
from django.urls import re_path

# Create your tests here.

app_name = 'web'

urlpatterns = [
    re_path(r'^spotlight/$', views.spotlight_view, name='spotlight'),
    re_path(r'^create-spotlight/$', views.create_spotlight_view, name='create_spotlight'),
    re_path(r'^edit-spotlight/(?P<pk>.*)/$', views.edit_spotlight_view, name='edit_spotlight'),
    re_path(r'^delete-spotlight/(?P<pk>.*)/$', views.delete_spotlight_view, name='delete_spotlight'),

    re_path(r'^news/$', views.news_list_view, name='news_list'),
    re_path(r'^news/(?P<pk>.*)/$', views.news_view, name='news'),
    re_path(r'^create-news/$', views.create_news_view, name='create_news'),
    re_path(r'^edit-news/(?P<pk>.*)/$', views.edit_news_view, name='edit_news'),
    re_path(r'^delete-news/(?P<pk>.*)/$', views.delete_news_view, name='delete_news'),

    re_path(r'^gallery/$', views.gallery_list, name='gallery_list'),
    re_path(r'^gallery/(?P<pk>.*)/$', views.gallery, name='gallery'),
    re_path(r'^create-gallery/$', views.create_gallery, name='create_gallery'),
    re_path(r'^edit-gallery/(?P<pk>.*)/$', views.edit_gallery, name='edit_gallery'),
    re_path(r'^delete-gallery/(?P<pk>.*)/$', views.delete_gallery, name='delete_gallery'),

    re_path(r'^testimonial/$', views.testimonial_list, name='testimonial_list'),
    re_path(r'^testimonial/(?P<pk>.*)/$', views.testimonial, name='testimonial'),
    re_path(r'^create-testimonial/$', views.create_testimonial, name='create_testimonial'),
    re_path(r'^edit-testimonial/(?P<pk>.*)/$', views.edit_testimonial, name='edit_testimonial'),
    re_path(r'^delete-testimonial/(?P<pk>.*)/$', views.delete_testimonial, name='delete_testimonial'),

    re_path(r'^vision/$', views.vision_list, name='vision_list'),
    re_path(r'^create-vision/$', views.create_vision, name='create_vision'),
    re_path(r'^edit-vision/(?P<pk>.*)/$', views.edit_vision, name='edit_vision'),
    re_path(r'^delete-vision/(?P<pk>.*)/$', views.delete_vision, name='delete_vision'),

    re_path(r'^mission/$', views.mission_list, name='mission_list'),
    re_path(r'^create-mission/$', views.create_mission, name='create_mission'),
    re_path(r'^edit-mission/(?P<pk>.*)/$', views.edit_mission, name='edit_mission'),
    re_path(r'^delete-mission/(?P<pk>.*)/$', views.delete_mission, name='delete_mission'),

    re_path(r'^management_team/$', views.management_team_list, name='management_team_list'),
    re_path(r'^management_team/(?P<pk>.*)/$', views.management_team, name='management_team'),
    re_path(r'^create-management_team/$', views.create_management_team, name='create_management_team'),
    re_path(r'^edit-management_team/(?P<pk>.*)/$', views.edit_management_team, name='edit_management_team'),
    re_path(r'^delete-management_team/(?P<pk>.*)/$', views.delete_management_team, name='delete_management_team'),

    re_path(r'^careers/$', views.careers_view, name='careers_list'),
    re_path(r'^create-career/$', views.create_careers_view, name='create_careers'),
    re_path(r'^edit-career/(?P<pk>.*)/$', views.edit_careers_view, name='edit_career'),
    re_path(r'^delete-career/(?P<pk>.*)/$', views.delete_careers_view, name='delete_career'),

    re_path(r'^allpied-careers/$', views.applied_careers_view, name='applied_careers'),

    re_path(r'^contact/$', views.contact_view, name='contact_list'),
    re_path(r'^create-contact/$', views.create_contact_view, name='create_contact'),
    re_path(r'^edit-contact/(?P<pk>.*)/$', views.edit_contact_view, name='edit_contact'),
    re_path(r'^delete-contact/(?P<pk>.*)/$', views.delete_contact_view, name='delete_contact'),

    re_path(r'^enquiry/$', views.enquiry_view, name='enquiry_list'),
]