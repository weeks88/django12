'''
Created on 2018. 12. 29.

@author: user
'''
from .models import Post
from django.forms.models import ModelForm
from django import forms
#글 등록에 사용할 폼클래스 - 모델폼클래스 상속
class PostForm(ModelForm):
    #사용자의 첨부파일, 이미지 업로드에 사용할 <input>을 커스텀 생성
    #required=False : 해당 <input>을 사용자가 필수로 입력하지 않아도 되는 공간 설정
    #ClearableFileInput : <input type='file'>형태의 입력공간에 추가설정을 할때 사용하는 위젯
    #attrs={'multiple' : True} : 하나의 입력공간에 여러개의 파일을 업로드 할 수 있도록 설정
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple':True}))
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model=Post
        fields=['type', 'headline', 'content']
#검색에 사용할 폼클래스 - 폼클래스 상속
class SearchForm(forms.Form):
    search_word=forms.CharField(max_length=200, label='검색어')