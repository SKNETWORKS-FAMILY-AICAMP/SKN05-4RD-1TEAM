from chatbot import views
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')), # 앱 URL 추가 
    path('', views.home, name='home'),  # 메인 페이지
    path('submit', views.submit, name='submit'),  # submit 경로 추가
    path('upload/', views.upload_pdf, name='upload_pdf'),
]
