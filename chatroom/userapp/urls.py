from django.conf.urls import url

from userapp import views

urlpatterns=[
    url(r'^login$',views.login),
    url(r'^register$',views.register),
    url(r'^register/check$',views.register_check),
    url(r'^logout$',views.logout),
    url(r'^modify$',views.modify),
]