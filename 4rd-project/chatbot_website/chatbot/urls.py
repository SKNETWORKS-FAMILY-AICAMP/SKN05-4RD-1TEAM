from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("signup/", views.signup_view, name="signup"),
    path("", views.HomeView.as_view(), name="home"),  # 홈 페이지 경로
    path("chat/", views.chat_view, name="chat"),  # 채팅 페이지
    path("upload_pdf/", views.upload_pdf, name="upload_pdf"),
    path("reset_chat/", views.reset_chat, name="reset_chat"),
    path("submit/", views.submit, name="submit"),  # 데이터 제출 처리
]
