from django.forms import ModelForm
from .models import User, Profile

from django.contrib.auth.forms import UserCreationForm


# form1
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


# form2
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
