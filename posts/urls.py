from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    # /posts/
    url(r'^$', views.post_list, name='list'),
    # /posts/create
    url(r'^create/$', views.post_create, name='create'),
    # /posts/<post_id>
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    # /posts/<post_id>/edit
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    # /posts/<post_id>/delete
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
]