from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import environ
from django.urls import reverse
from rest_framework import status
env = environ.Env()
from .models import User
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,AgentSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegistrationForm, AgentRegistrationForm, LoginForm

#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def custom_404_page(request, exception):
    return render(request, 'views/404.html', status=404)
    
class SignupCreateView(APIView):
    def get(self, request, *args, **kwargs):
        domain = env('DOMAIN')
        form = RegistrationForm()
        context = {
            'domain': domain,
            'form': form,  # Initialize an empty registration form
        }
        return render(request, 'views/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.data, request.FILES)  # Use request.data for POST data
        if form.is_valid():
            # If the form is valid, save the user
            user = form.save()
            # You may want to log the user in here, or send a confirmation email
            return redirect('/join-now/?success=True')  # Replace 'success_url' with your desired success URL
        else:
            # If the form is not valid, re-render the registration form with errors
            domain = env('DOMAIN')
            context = {
                'domain': domain,
                'form': form,  # Include the form with validation errors
            }
            return render(request, 'views/signup.html', context)

class AgentSignUpView(APIView):
    def get(self, request):
        # Render the agent registration form
        domain = env('DOMAIN')
        context = {
            'domain': domain,
            'form': AgentRegistrationForm(),  # Use the AgentRegistrationForm
        }
        return render(request, 'views/signup.html', context)

    def post(self, request):
        form = AgentRegistrationForm(request.data, request.FILES)  # Use AgentRegistrationForm
        if form.is_valid():
            # If the form is valid, save the agent
            agent = form.save()
            # You may want to log the agent in here or send a confirmation email
            return redirect('/agent-signup/?success=True')  # Replace 'success_url' with your desired success URL
        else:
            # If the form is not valid, re-render the agent registration form with errors
            domain = env('DOMAIN')
            context = {
                'domain': domain,
                'form': form,  # Include the form with validation errors
            }
            return render(request, 'views/signup.html', context)


class SignUpFromAgentView(APIView):
    def get(self, request, uuid_param):
        print('here')
        # Check if the agent with the provided UUID exists, or return a 404 page
        agent = get_object_or_404(User, id=uuid_param)

        # Create a form instance and pre-fill the 'from_agent' field with the agent's UUID
        form = RegistrationForm(initial={'from_agent': agent.id})

        # Now you have access to the agent object and a pre-filled form
        domain = env('DOMAIN')
        context = {
            'domain': domain,
            'agent': agent,
            'form': form,
        }
        return render(request, 'views/signup.html', context)

    def post(self, request, uuid_param):
        # Check if the agent with the provided UUID exists, or return a 404 page
        agent = get_object_or_404(User, id=uuid_param)

        # Create the form instance with the data and files from the request
        form = RegistrationForm(request.data, request.FILES)

        if form.is_valid():
            # If the form is valid, save the user with the associated agent
            user = form.save(commit=False)
            user.from_agent = agent  # Associate the user with the agent
            user.save()
            # You may want to log the user in here or send a confirmation email
            # You may want to log the user in here or send a confirmation email
            success_url = reverse('join-now', kwargs={'uuid_param': uuid_param})
            success_url += '?success=True'  # Append the success parameter
            return redirect(success_url)  # Replace 'success_url' with your desired success URL
        else:
            # If the form is not valid, re-render the registration form with errors
            domain = env('DOMAIN')
            context = {
                'domain': domain,
                'agent': agent,
                'form': form,  # Include the form with validation errors
            }
            return render(request, 'views/signup.html', context)


class UserRegistrationByEasyView(APIView):
    def post(self, request):
      try:
         serializer = UserRegistrationSerializer(data=request.data)

         if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({"erros": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponse

class LoginView(APIView):
    def get(self, request, uuid_param):

        # Check if the agent with the provided UUID exists, or return a 404 page
        agent = get_object_or_404(User, id=uuid_param)

        # Create a form instance and pre-fill the 'from_agent' field with the agent's UUID
        form = LoginForm()

        # Now you have access to the agent object and a pre-filled form
        domain = env('DOMAIN')
        context = {
            'domain': domain,
            'form': form,
        }
        return render(request, 'views/login.html', context)

    def post(self, request, uuid_param):
        # Check if the agent with the provided UUID exists, or return a 404 page
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
              tokens = get_tokens_for_user(user)
              response = HttpResponse("Login successful")

              # Set the JWT token as an HTTP-only cookie
              response.set_cookie(key='access_token', value=tokens['access'], httponly=True)
              if user.is_agent: 
                  return redirect('/affiliate/')
              elif user.is_admin: 
                  return redirect('/admin/')
              else:
                  return redirect('/login/')
        # If the form is invalid or authentication fails, re-render the login page with errors
        return render(request, 'login.html', {'form': form, 'login_error': True})
        

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

from rest_framework.views import APIView
from .models import User

class AgentListView(generics.ListAPIView):
    queryset = User.objects.filter(is_agent=True)  # Use queryset instead of get_queryset
    serializer_class = AgentSerializer

class SignUpView(APIView):
     def get(self, request):
        domain =  env('DOMAIN')
        context = {
            'domain': domain,
        }
        return render(request, 'views/signup.html',context)

