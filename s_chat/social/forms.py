
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Tweep  




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control col-sm-10'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control col-sm-10'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control col-sm-10'}),
        }




class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class TweeForm(forms.ModelForm):
        body =forms.CharField(required=True,            widget=forms.widgets.Textarea(
                    attrs={
                        "placeholder": "Enter Your Tweep", "class": "form-control",
                    }
                ),label="")
        class Meta:
            model = Tweep
            exclude = ("user"),
            
            
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    
    first_name = forms.CharField(label="", required=True,max_length= 100, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}))
    
    last_name = forms.CharField(label="", required=True,max_length= 100, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email", "password1","password2")
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] ='User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text-muted"><small>Required. 150 characters or fewer. letters, digits and special caracters</small></span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] ='Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text-muted"><small>Required. 8 characters with atleast 1 capital letter and 1 special character @,#,$,%,&,_!?</small></span> '
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] ='Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text-muted"><small>Enter the same password as before , for verification</small></span>'