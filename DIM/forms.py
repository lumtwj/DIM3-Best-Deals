from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from BestBuy.models import UserProfile
class BestBuyRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.Field(required=True)
    last_name=forms.Field(required=True)
    address=forms.forms.Field(required=True)
    handphone=forms.Field(required=True)
    postalcode=forms.Field(required=True)
    class Meta:
      model = User
      fields = ('username','password1','password2')
    def save(self, commit=True):
      user = super(BestBuyRegistrationForm, self).save(commit=True)
      user_profile =UserProfile(user=user,email=self.cleaned_data['email'],first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'],address=self.cleaned_data['address'],handphone=self.cleaned_data['handphone'],postalcode=self.cleaned_data['postalcode'])
      if commit:
       user_profile.save()
       user.save()
      return user,user_profile

class editProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email','first_name','last_name','address', 'handphone','postalcode')