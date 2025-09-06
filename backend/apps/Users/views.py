from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

# Create your views here.

User = get_user_model()

# Convert to dictionary
ROLE_PRIORITY = ["admin", "faculty", "staff", "org_officer", "student"] 
'''


    choices = {
1:'ADMIN',
2:'STUDENT'
}


user.choices(choices)

serilazer

role.charfield(choices.data)

'''

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('username') 
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'message': 'Username/email and password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=identifier, password=password)

        if user is None and '@' in identifier:
            try:
                u = User.objects.get(email__iexact=identifier)
                user = authenticate(username=u.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'message': 'Account is inactive'}, status=status.HTTP_403_FORBIDDEN)

        # retreieve roles fdrom database
        roles = list(user.groups.values_list('name', flat=True))
        # an AI-improved primary role evaluator
        primary_role = next((r for r in ROLE_PRIORITY if r in roles), None)

        refresh = RefreshToken.for_user(user)

        # details are returned like this
        return Response({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'roles': roles,
            'primary_role': primary_role,
            'username': user.username,
        }, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    
    # Handles fetching and updating the user profile.
    # This requires the user to be authenticated.
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(profile_data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()

        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

class UserRegistrationAPIView(APIView):
    """
    Handles user registration (creating a new user).
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"message": "Username, password, and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        return Response({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)
