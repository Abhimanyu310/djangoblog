from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    # /posts/
    url(r'^$', views.post_list, name='list'),
    # /posts/create
    url(r'^create/$', views.post_create, name='create'),
    # /posts/<post_id>
    url(r'^(?P<post_id>\d+)/$', views.post_detail, name='detail'),
    # /posts/<post_id>/edit
    url(r'^(?P<post_id>\d+)/edit/$', views.post_update, name='update'),
    # /posts/<post_id>/delete
    url(r'^(?P<post_id>\d+)/delete/$', views.post_delete, name='delete'),
]