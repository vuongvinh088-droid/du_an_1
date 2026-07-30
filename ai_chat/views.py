import os
from django.shortcuts import render
from django.http import JsonResponse
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo client Gemini SDK mới
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chat_home(request):
    return render(request, 'ai_chat/chat.html')

def get_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        if not user_message:
            return JsonResponse({"error": "Tin nhắn không được để trống"}, status=400)
        
        try:
            # Mã model chuẩn duy nhất cho SDK google-genai hiện tại:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_message,
            )
            return JsonResponse({"reply": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)