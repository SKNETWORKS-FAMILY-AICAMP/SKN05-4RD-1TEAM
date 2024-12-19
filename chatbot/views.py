import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm
from django.conf import settings
from PyPDF2 import PdfReader
from .models import load_file_and_split, create_vector_store, rag_chain
from django.views.decorators.csrf import csrf_exempt
import tempfile
from django.http import FileResponse
import json


# 홈 페이지
def home(request):
    """
    홈페이지를 렌더링합니다.
    """
    return render(request, "home.html")

# 회원가입 페이지
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # 회원가입 후 로그인 페이지로 이동
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

# 로그인 페이지
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("chat")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect("login")

# 채팅 페이지 (로그인 필요)
@login_required
def chat_view(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        if user_input:
            response = f"🚀 AI 답변: {user_input}에 대한 답변입니다."
            chat_history = request.session["chat_history"]
            chat_history.append({"user": user_input, "bot": response})
            request.session["chat_history"] = chat_history
    return render(request, "chat.html", {"chat_history": request.session["chat_history"]})

# 대화 기록 초기화
@login_required
def reset_chat(request):
    if "chat_history" in request.session:
        del request.session["chat_history"]
    return redirect("chat")


# 데이터 제출 처리
@login_required
def submit(request):
    """
    사용자가 데이터를 제출하면 처리합니다.
    """
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        response_data = {"response": f"✅ {user_input}를 처리했습니다."}
        return JsonResponse(response_data)
    return render(request, "chat.html", {"error": "잘못된 요청입니다."})

class HomeView(TemplateView):
    template_name = 'home.html'

qa_chain = None  # 전역 변수로 QA 체인 저장

@login_required
@csrf_exempt
def upload_pdf(request):
    global qa_chain
    try:
        if request.method == "POST" and request.FILES.get("pdf_file"):
            pdf_file = request.FILES["pdf_file"]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            chunks = load_file_and_split(temp_file_path)
            vector_store = create_vector_store(pdf_file.name, chunks)
            qa_chain = rag_chain(vector_store)

            return JsonResponse({"status": "success", "message": "PDF 처리 완료"})
        return JsonResponse({"status": "fail", "message": "파일 업로드 실패"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "fail", "message": str(e)}, status=500)

@csrf_exempt
def chat_view(request):
    global qa_chain

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_input = data.get("user_input", "").strip()

            if not user_input:
                return JsonResponse({"status": "fail", "message": "질문이 없습니다."}, status=400)

            if qa_chain is None:
                return JsonResponse({"status": "fail", "message": "PDF를 먼저 업로드하세요."}, status=400)

            response = qa_chain.run(user_input)
            return JsonResponse({"status": "success", "response": response})

        except json.JSONDecodeError:
            return JsonResponse({"status": "fail", "message": "잘못된 요청 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "fail", "message": f"오류 발생: {str(e)}"}, status=500)

    if request.method == "GET":
        return render(request, "chat.html", {"chat_history": request.session.get("chat_history", [])})