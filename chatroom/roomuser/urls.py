from django.conf.urls import url

from roomuser import views

urlpatterns=[
    url(r'^set$',views.setView),
    url(r'^get$',views.getView),
    url(r'^out$',views.outView),
    url(r'^transfer$',views.transferView),

]