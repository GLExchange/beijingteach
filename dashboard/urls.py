from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^login/$',
        views.login_user, name='login_user'),
    url(r'^pages/$',
        views.pages, name='pages'),
    url(r'^images/$',
        views.images, name='images'),
    url(r'^applicants/$',
        views.applicants, name='applicants'),
    url(r'^pages/new/$',
        views.new_page, name='new_page'),
    url(r'^pages/(?P<page_id>\d+)/$',
        views.update_page, name='update_page'),
    url(r'^pages/preview/(?P<page_id>\d+)/$',
        views.preview_page, name='preview_page'),
    url(r'^images/new/$',
        views.new_images, name='new_images'),
]
