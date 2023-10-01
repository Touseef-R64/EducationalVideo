from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import environ
from rest_framework import status
env = environ.Env()

from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer

class UserRegistrationByEasyView(APIView):
    def post(self, request):
      try:
         serializer = UserRegistrationSerializer(data=request.data)

         if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({"erros": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BASE(APIView):
     def get(self, request):
        # landmarks = Landmark.objects.all()
        # descriptions = Description.objects.all()

        # landmark_serializer = LandmarkSerializer(landmarks, many=True)
        # description_serializer = DescriptionSerializer(descriptions, many=True)
        domain =  env('DOMAIN')
        context = {
            'domain': domain,
        }
        return render(request, 'views/index.html',context)

