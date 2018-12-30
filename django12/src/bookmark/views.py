from django.shortcuts import render
from django.template.context_processors import request

#View : 사용자의 요청에 따라 데이터를 처리하고 HTML 문서나 새로운 URL 주소를 전송하는 역할

#View : 클래스/함수 형태로 정의

#함수 형태로 정의시 첫번째 매개변수를 request로 정의해야 함
#request : 사용자의 요청정보, <form>으로 넘겨준 데이터, 로그인 정보, 세션정보, 요청방식(GET,POST)

#HTML파일을 전송하는 메인페이지
def index(request):
    #render(request, HTML문서의 경로, HTML문서에 전달할 값(사전형))
    return render(request, 'bookmark/index.html', {'a':'Hello', 'b':[1,2,3]})

#모델클래스에 저장된 객체들을 추출하기 위해서 모델클래스 임포트
from .models import Bookmark
#from bookmark.models import Bookmark

#Bookmark 모델 클래스의 객체를 추출해 HTML 파일을 수정하는 페이지
def booklist(request):
    #모델클래스명.objects.all(): 데이터베이스에 해당 모델클래스로 저장된 모든 객체를 리스트 형태로 추출
    #모델클래스명.objects.get(): 데이터베이스에 해당 모델클래스로 저장된 객체중 한개를 추출
    #모델클래스명.objects.filter(): 데이터베이스에 특정조건을 만족하는 객체들을 리스트 형태로 추출
    #                .exclude() : 데이터베이스에 특정조건을 만족하지 않는 객체들을 리스트 형태로 추출
    objs = Bookmark.objects.all() #데이터베이스에 저장된 Bookmark 객체들을 모두 추출해 리스트 형태로 반환
    print(objs)
    
    return render(request, 'bookmark/booklist.html',{'objs' : objs})

#Bookmark 객체 중 하나의 데이터만 추출하는 페이지
# - 사용자가 선택한 객체를 구분하기 위해 새로운 매개변수를 사용
# - request를 제외한 매개변수는 URL등록시 특정부분을 매개변수에 전달하는 처리를 해줘야 함
def bookdetail(request, bookid):
    #데이터베이스에 저장된 Bookmark 객체중 사용자가 요청한 객체를 추출
    #get(조건) : 조건에 맞는 객체 한개를 가져옴 
    # - 조건에 맞는 객체가 여러개인 경우 -> 에러, - 조건에 맞는 객체가 없는 경우 -> 에러
    obj = Bookmark.objects.get(id=bookid)
    #추출한 객체와 HTML문서를 클라이언트에게 전달
    return render(request, 'bookmark/bookdetail.html', {'obj':obj})
    



