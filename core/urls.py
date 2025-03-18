from django.urls import path

from . import views


urlpatterns = [
  # path('', views.index, name='test'),
  path('signup/', views.signup, name='signup'),
  path('signin/', views.signin, name='signin'),
  path('logout/', views.logout, name='logout'),
  path('settings/', views.settings, name='settings'),
  path('upload/', views.upload, name='upload'),
  path('like-post/', views.like_post, name='like-post'),
  path('profile/<int:pk>/', views.profile, name='profile'),
  path('follow/', views.follow, name='follow'),
  path('search/', views.search, name='search'),
  path('searchJson/', views.searchJson, name='searchJson'),
  path('Message/', views.message, name='message'),
  path('Chat/<str:pk>', views.chat, name='chat'),
  path('', views.home, name='index'),
  path('updateprofile/', views.updateprofile, name='updateprofile'),
  path('Jsonchat/', views.Jsonchat, name='Jsonchat'),
  path('Chatting/<str:pk>', views.Chatting, name='Chatting'),
  
  



]
