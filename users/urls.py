from django.urls import path
from . import views
urlpatterns = [
   path('', views.BASE.as_view(), name='home'),
   path('join-now/', views.SignupCreateView.as_view(), name='sign-up-create'),
   path('join-now/<uuid:uuid_param>/', views.SignUpFromAgentView.as_view(), name='signup-from-agent'),
   path('agent-signup/', views.AgentSignUpView.as_view(), name='agent-signup'),
   path('agents/', views.AgentListView.as_view(), name='agent-list'),
   path('login/', views.LoginView.as_view(), name='login'),
]