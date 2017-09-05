from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^/traer_facultades$', csrf_exempt(views.traer_facultades), name = 'traer_facultades')
]
