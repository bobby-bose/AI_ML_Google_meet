
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('results/<str:text>/', views.results, name='results'),
    path('home/', views.home, name='home'),
    path('camera/', views.camera, name='camera'),
    path('schedule-meeting/', views.schedule_meeting, name='schedule_meeting'),
   path('detect_eyes/', views.detect_eyes, name='detect_eyes'),
    path('detect_face/', views.detect_faces, name='detect_face'),
    path('voice_detection/', views.voice_detection, name='voice_detection'),
]