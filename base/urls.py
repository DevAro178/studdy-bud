from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('login/', views.loginPage,name="login"),
    path('register/', views.RegisterPage,name="register"),
    path('logout/', views.logoutPage,name="logout"),
    path('room/<str:pk>/', views.room,name="room"),
    path('profile/<str:pk>/', views.user_profile,name="user-profile"),
    path('setting/', views.userSetting,name="update-user"),
    path('create-room/', views.createroom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('browse-topics/',views.browseTopics,name="browse-topics"),
    path('activity-feed/',views.activityFeed,name="activity-feed"),
    
]
