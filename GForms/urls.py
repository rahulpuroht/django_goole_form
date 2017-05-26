from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from GForms import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

appname = 'GForms'
# ******* WEBSITE URL ********
urlpatterns = [
	url(r'^$', views.landingpage,  name="home"),
	url(r'^login$', views.login),
	url(r'^signup$', views.signup),
	url(r'^addform$', views.addform),
	url(r'^answertype$', views.answerType),
	url(r'^addquestion$', views.addquestion),
	url(r'^allforms$', views.allforms),
	url(r'^yourforms$', views.yourforms),
	url(r'^saveResponse$', views.saveResponse),
]