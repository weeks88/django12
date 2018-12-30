'''
Created on 2018. 12. 23.

@author: user
'''
from django.forms import ModelForm
#django.contrib.auth 어플리케이션의 models.py에서 User모델 클래스를 임포트
#User 모델 클래스 : django에서 제공하는 기본적인 회원관리 클래스
from django.contrib.auth.models import User
from django import forms
#회원가입에 사용할 모델 폼 클래스
class SignupForm(ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_check'].label = "패스워드 확인"
    #폼 클래스에서 추가적인 <input>을 만들경우 forms.XXXField 객체를 변수에 저장
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    #<input>의 순서를 지정하는 변수
    field_order = ['username', 'password', 'password_check', 'last_name', 'first_name', 'email'] 
    class Meta:
        model = User
        #input 태그에 특정한 type을 지정할  때 사용
        #필드이름을 키값, 저장할 값은 forms.XXXInput클래스의 객체를 저장
        widgets={
            #password <input>태그에 비밀번호 type을 지정해줌
            'password':forms.PasswordInput()
            }
        #ID, 비밀번호, 성, 이름, 이메일
        fields = ['username', 'password', 'last_name', 'first_name', 'email']

#로그인에 사용할 모델 폼 클래스
class SigninForm(ModelForm):
    class Meta:
        model = User
        widgets={
            #password <input>태그에 비밀번호 type을 지정해줌
            'password':forms.PasswordInput()
            }
        fields=['username', 'password']