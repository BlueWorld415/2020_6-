from django.conf.urls import url

from notice import views

urlpatterns=[
    url(r'^send$',views.send),
    url(r'^get$',views.get),
    url(r'^new$',views.new),


]