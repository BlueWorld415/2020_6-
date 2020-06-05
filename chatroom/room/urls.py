from django.conf.urls import url

from room import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^index$',views.index),
    url(r'^room$',views.room),
    url(r'^chat$',views.chat),
    url(r'^upload$',views.upload),
    url(r'^files$',views.files),
    url(r'^files/remove',views.remove),
    url(r'^dissolution',views.dissolution),
    url(r'^leave',views.leave),
]
