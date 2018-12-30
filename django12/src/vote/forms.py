'''
Created on 2018. 12. 22.

@author: user
'''
#form : HTML 코드에서 사용할 입력양식(<form><input>)을 모델클래스에 맞게 (또는 커스텀)자동으로 만드는 기능

#class 클래스명(ModelForm 또는 Form):
#ModelForm : 모델클래스를 기반으로 입력양식을 자동 생성할 때 상속받는 클래스
#Form : 커스텀 입력양식을 생성할 때 상속받는 클래스

#폼 클래스의 객체를 함수를 이용해서 HTML문서의 입력양식으로 변환할 수 있음(<p>, <table>, <li>)

#1)ModelForm 클래스 임포트      2)사용하고자 하는 모델클래스 임포트    3) ModelForm을 상속받은 폼클래스를 정의

# 어플리케이션 제작하는 순서
# 기존) 어플리케이션 생성 -> setting.py등록 -> 모델정의 -> 데이터베이스 반영 -> 뷰 정의 ->템플릿 정의 -> url등록
# 변경) 어플리케이션 생성 -> setting.py등록 -> 모델정의 -> 폼클래스 정의 -> 데이터베이스 반영 -> 뷰 정의 ->템플릿 정의 -> url등록

from django.forms.models import ModelForm
from .models import Question, Choice

#Question 모델클래스와 연동된 모델폼클래스 정의
class QuestionForm(ModelForm):
    class Meta: #Meta 클래스 : 모델클래스에 대한 정보를 정의하는 클래스 (고정된 명칭임)
        #model : 어떤 모델클래스와 연동할지 저장
        #fields : 모델클래스에 정의된 변수중 어떤 변수를 클라이언트가 작성할 수 있도록 입력양식을 만들것인지 저장하는 변수(iterable)
        #exclude : 모델클래스에 정의된 변수 중 입력양식으로 만들지 않을 것을 정의하는 변수
        #fields, exclude 변수 중 한개만 사용해야 함
        model = Question
        fields = ['name']
        #exclude = ['date']
#Choice 모델클래스와 연동된 모델폼 클래스 정의
class ChoiceForm(ModelForm):
    #'q'변수의 <label>태그의 값을 변경
    def __init__(self, *args, **kwarg):
        #ModelForm 클래스의 생성자를 호출해 모델폼 기능을 사용할 수 있도록 초기화
        super().__init__(*args, **kwarg)
        #q 라벨 이름 변경
        self.fields['q'].label = '질문지'
    class Meta:
        model = Choice
        fields = ['q', 'name']
        #exclude=['votes']         