
import re
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .utils import lookup

class registration(forms.Form):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(
                                               attrs={'placeholder':'Username',
                                                      'class':'form-control'}),
                               validators=[RegexValidator(
                                               regex='^($|[a-z]{1}[a-z0-9_]{3,13}$)',
                                               message='Must start with an lowercase alphabet and '
                                                       'should be of 4 to 14 characters long.')])
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(
                                               attrs={'render_value':False,
                                                      'placeholder':'Password',
                                                      'class':'form-control'}),
                               validators=[RegexValidator(
                                               regex='^[a-zA-Z0-9!#$%&?"]{6,30}$',
                                               message='Password length should between 6 and 30.'
                                                       'Allowed Symbols: !#$%&?"')])
    passwordConfirm = forms.CharField(required=True,
                                      widget=forms.PasswordInput(
                                                      attrs={'render_value':False,
                                                             'placeholder':'Password (again)',
                                                             'class':'form-control'}))


    def clean_username(self):
        # To check Username exists or not and accordingly continue
        usern=None
        user_query = None
        if 'username' in list(self.cleaned_data.keys()):
            usern = self.cleaned_data['username']
        try:
            user_query = User.objects.get(username__iexact=usern)
        except:
            return self.cleaned_data['username']
        else:
            raise forms.ValidationError('Username Already Exists. Please try another username.')

    def clean(self):
        #password matching
        if 'password' in self.cleaned_data and 'passwordConfirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['passwordConfirm']:
                raise forms.ValidationError('Entered Passwords didn\'t Match. Please try Again.')
            else:
                return self.cleaned_data


class loginForm(forms.Form):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(
                                               attrs={'placeholder':'Username',
                                                      'class':'form-control'}),
                               validators=[RegexValidator(
                                               regex='^($|[a-z]{1}[a-z0-9_]{3,13}$)',
                                               message='Must start with an lowercase alphabet and '
                                                       'should be of 4 to 14 characters long.')])
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(
                                               attrs={'render_value':False,
                                                      'placeholder':'Password',
                                                      'class':'form-control'}),
                               validators=[RegexValidator(
                                               regex='^[a-zA-Z0-9!#$%&?"]{6,30}$',
                                               message='Password length should between 6 and 30. '
                                                       'Allowed Symbols: !#$%&?"')])

    def clean(self):
        try:
            userAuth = authenticate(username=self.cleaned_data['username'],
                                    password=self.cleaned_data['password'])
        except:
            pass
        else:
            if userAuth is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError('Incorrect username or password.')


class quoteForm(forms.Form):
     symbol = forms.CharField(required=True,
                              widget=forms.TextInput(
                                               attrs={'placeholder':'Symbol',
                                                      'class':'form-control'}),
                              validators=[RegexValidator(
                                               regex='^[A-Z0-9-]+(\.[A-Z]+)?$',
                                               message='Enter the symbol in Block Letters.')])


class buyAndSellForm(forms.Form):
     symbol = forms.CharField(required=True,
                              widget=forms.TextInput(
                                               attrs={'placeholder':'Symbol',
                                                      'class':'form-control'}),
                              validators=[RegexValidator(
                                               regex='^[A-Z0-9-]+(\.[A-Z]+)?$',
                                               message='Invalid symbol.')])

     shares = forms.IntegerField(required=True,
                                 widget=forms.TextInput(
                                           attrs={'placeholder':'Shares',
                                                  'class':'form-control'}),
                                 validators=[RegexValidator(
                                                 regex='^[1-9]\d*$',
                                                 message='Enter a valid number of shares.')])

     def clean(self):
         if 'symbol' not in self.cleaned_data or 'shares' not in self.cleaned_data:
             return self.cleaned_data # 'required=True' attribute will handle the case
         else:
             info = lookup(str(self.cleaned_data['symbol']))
             self.cleaned_data['stockInfo'] = info
             if not info['exists']:
                 raise forms.ValidationError('Invalid Symbol.')
             if self.cleaned_data['shares'] < 1:
                 raise forms.ValidationError('Invalid number of shares.')
             return self.cleaned_data


