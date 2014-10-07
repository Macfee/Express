# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    用户login类，从Form类继承
    """
    #email
    email = forms.EmailField(label='电子邮件')
    #passwd
    password = forms.CharField(label='密码',max_length=20,widget=forms.PasswordInput())
    #是否记住登录
    remember = forms.BooleanField(label='下次自动登录',required=False)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            #判断email是否被注册
            User.objects.get(email = self.cleaned_data['email'])
        except Exception, e:
            raise forms.ValidationError('该email不存在或密码错误，请重新填写！')
        return email
    
    def clean_password(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            password=self.cleaned_data['password']
            
            u = User.objects.get(email = email)
            user = auth.authenticate(username=u.username,password=password)
            if user is not None and user.is_active:
                return password
        
            raise forms.ValidationError('该email不存在或密码错误，请重新填写！')
