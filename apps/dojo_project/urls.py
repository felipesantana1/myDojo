from django.conf.urls import url
import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^addUser$', views.create),
    url(r'^login$', views.login),
    url(r'^trips$', views.trips),
    url(r'^destination/(?P<id>\d+)$', views.display),
    url(r'^trips/add$', views.plan),
    url(r'^addTrip$', views.addTrip),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home)

]