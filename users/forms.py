from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email","first_name","last_name",'payment_picture', 'contact', 'address')
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'payment_picture': 'Payment Reciept',
            'contact': 'Contact Number', 
            'address': 'Address'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'example@.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ali'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ahmed'}),
            'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '03**-********'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country, city, street xyz, house 123'}),
            'payment_picture': forms.FileInput(attrs={'class': 'main-btn'})
        }

    def save(self, commit=True):
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first=self.cleaned_data['first_name'],
                last=self.cleaned_data['last_name'],
                payment_picture=self.cleaned_data['payment_picture'],
                contact=self.cleaned_data['contact'], 
                address= self.cleaned_data['address'],
            )

            if commit:
                user.save()

            return user

class AgentRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "payment_picture",'is_agent')
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'payment_picture': 'Payment Reciept'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'example@.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ali'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ahmed'}),
            'payment_picture': forms.FileInput(attrs={'class': 'main-btn'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_agent'].initial = True
        self.fields['is_agent'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first=self.cleaned_data['first_name'],
                last=self.cleaned_data['last_name'],
                payment_picture=self.cleaned_data['payment_picture'],
                is_agent=self.cleaned_data['is_agent']
            )

            if commit:
                user.save()

            return user

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
        labels = {
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'example@.com'}),
            'password': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '*********'}),
            }

