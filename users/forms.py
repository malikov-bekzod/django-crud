from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password","image",)
   

    def save(self,commit = True):
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
    
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","password")