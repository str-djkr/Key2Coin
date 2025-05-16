from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserActivity, LandingPage
from .serializers import UserSerializer, UserActivitySerializer
import re


from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# API View
class RegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        print(213321)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

# Web View
# @csrf_exempt
# def register_view(request):
#     if request.method == 'POST':
#         # Обробка форми реєстрації
#         return redirect('landing')
#     return render(request, 'register.html')

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create initial activity
        UserActivity.objects.create(user=user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)


class KeystrokeLogAPIView(generics.CreateAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        keystrokes = request.data.get('keystrokes', 0)
        source_app = request.data.get('source_app', None)

        # Anti-cheat and validation would go here
        coins_earned = keystrokes / 100  # Simplified calculation

        # Update user stats
        user.total_keystrokes += keystrokes
        user.total_coins += coins_earned
        user.update_streak()
        user.save()

        # Log activity
        activity = UserActivity.objects.create(
            user=user,
            keystrokes=keystrokes,
            coins_earned=coins_earned,
            source_app=source_app
        )

        return Response({
            "coins_earned": coins_earned,
            "total_coins": user.total_coins,
            "streak": user.current_streak
        }, status=status.HTTP_201_CREATED)



def register_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('email')

            email = request.POST.get('email')
            password = request.POST.get('password')

            # Проста валідація
            if not all([username, email, password]):
                messages.error(request, "Будь ласка, заповніть всі поля")
                return render(request, 'register.html')

            # Створення користувача
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Автоматичний вхід
            login(request, user)
            return redirect('landing')

        except Exception as e:
            messages.error(request, f"Помилка реєстрації: {str(e)}")
            return render(request, 'register.html')

    # GET-запит - показати форму
    return render(request, 'register.html')


def landing_view(request):
    landing = LandingPage.objects.filter(is_active=True).first()
    context = {'landing': landing or LandingPage()}
    return render(request, 'landing.html', context)