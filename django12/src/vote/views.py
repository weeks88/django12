from django.shortcuts import render, get_object_or_404
from .models import Question, Choice

from django.http.response import HttpResponseRedirect
from django.urls import reverse
from setuptools._vendor.six import _urllib_request_moved_attributes

#HTML문서를 넘겨주는 것이 아닌 리다이렉트 주소를 넘겨줄때 HttpResponseRedirect 클래스의 객체를 반환하면 됨
#HttpResponseRedirect(사용자에게 넘겨줄 주소(문자열))
#reverse :템플릿의 url태그와 동일한 기능을 수행, 별칭을 기반으로 한 URL검색
#reverse(등록된 별칭(문자열), args=(매개변수에 넘겨줄 값,))

# HttpResponseRedirect(reverse())
 
# Create your views here.
#index(질문리스트)
def index(request):
    #Question 객체를 추출
    a = Question.objects.all()
    #HTML문서에 객체 리스트 전달후 클라이언트에게 HTML파일 전송
    return render(request, 'vote/index.html', {'a':a})
#detail(질문 선택시 답변항목 제공)
def detail(request, qid):
    # get_object_or_404(모델클래스, 조건) : 해당 모델클래스에서 조건에 맞는 객체 한개 추출
    # 조건에 맞는 객체가 한개도 없는 경우, 사용자가 잘못요청한 것으로 처리해 404에러를 띄우는 처리를 해줌
    b = get_object_or_404(Question, id=qid) #Question.objects.get(id=qid)
    return render(request, 'vote/detail.html', {'q':b})
#vote(웹 클라이언트 요청에 따라 투표적용)
def vote(request):
    #POST방식으로 사용자가 요청했는지 확인
    #request.method : 사용자의 요청방식이 문자열 형태로 저장되 변수
    if request.method == "POST":
        #request.POST : POST방식으로 요청하면서 넘어온 데이터(사전형)
        #request.POST.get(키값) : POST방식으로 넘어온 데이터 중 입력한 키값과 동일한 데이터를 추출
        c_id = request.POST.get('a') #request.POST['a']
        c = get_object_or_404(Choice, id = c_id)
        c.votes += 1
        c.save() #변동사항을 데이터베이스에 반영
        
        #vote어플리케이션의 index뷰로 이동할수 있도록 URL주소를 넘겨줌
        return HttpResponseRedirect(reverse('vote:result', args=(c.q.id,)))
        #c.q : Choice 객체 c에 저장된 q를 접근 -> c와 연결된 Question객체 자체를 의미
        #c.q.id : Choice 객체 c와 연결된 Question 객체의 id변수값을 가져옴
                
#result(투표결과)
def result(request, q_id):
    return render(request, 'vote/result.html', {'q':get_object_or_404(Question, id=q_id)})

from .forms import QuestionForm, ChoiceForm
from _datetime import datetime # 현재 날짜/시간을 불러오는 파이썬 내장 함수
from django.contrib.auth.decorators import login_required
#데코레이터 : URL요청에 따라 뷰함수를 호출하는데, 호출전에 데코레이터가 먼저 실행되서 초기화 작업, 로그인 확인, 접근권한 확인을 수행하는 기능
#함수에 데코레이터 붙이기
#@데코레이터 함수 이름
#클래스에 데코레이터 붙이기
#class Class(사용할 데코레이터 클래스명)

#login_required : 뷰함수 호출전 요청을 한 클라이언트가 로그인을 했는지 여부를 파악하고
#비로그인 상태인 경우 로그인페이지를 띄워주는 데코레이터 
# Question 객체를 사용자가 등록하는 뷰
@login_required
def qregister(request):
    #GET방식 처리
    if request.method == 'GET':
        #모델폼클래스 객체 생성
        #모델폼클래스 객체 생성시 매개변수에 값을 전달하지 않는 경우, 입력양식에 값이 비어있는 형태로 객체가 생성됨
        form = QuestionForm()
        #HTML파일 전달
        return render(request, 'vote/qregister.html',{'f':form})
    
    #POST방식 처리
    elif request.method == "POST":
        #사용자 요청정보를 받아 데이터베이스에 저장
        #request.POST : 사용자가 POST방식으로 요청했을때 같이 넘어온 데이터 집합(사전형)
        print(request.POST)
        #사용자 입력을 해당 폼객체 생성시 넣음
        form = QuestionForm(request.POST)
        if form.is_valid(): #사용자가 입력한 값이 유효한 값인지 확인
            #폼객체.cleaned_data : is_valid()함수로 유효한 값인지 확인후 True값을 반환했을때,
            #사용자의 입력정보를 확인할 수 있는 사전형 변수
            #폼객체.save() : 모델폼클래스의 객체만 사용가능. 연동된 모델클래스의 객체로 변환후 데이터베이스에 저장
            #폼객체.save(commit=False) : 연동된 모델클래스의 객체로 변환만 해줌
            
            #Question 객체는 date변수에 값이 비어있으면 안되므로 파이썬 코드로 data변수값을 채운후 DB에 저장해야 함
            q=form.save(commit=False) #q : form에 저장된 값을 바탕으로 생성된 Question객체
            print('생성된 question객체', q)
            q.date = datetime.now() #파이썬 모듈을 이용해 현재시간을 생성된 Qestion객체의 date변수에 저장
            q.save() #해당 Question객체를 데이터베이스에 저장함
            
            return HttpResponseRedirect(reverse('vote:index'))

# Choice 객체를 사용자가 등록하는 뷰
@login_required
def cregister(request):
    if request.method == 'GET':
        return render(request, 'vote/cregister.html',{'f':ChoiceForm()})
    elif request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            #더이상 비어있는 변수가 없으므로 데이터베이스 저장과 객체 변환을 동시에 실행
            c = form.save()
            print(c)
            return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,)))
        else: #사용자의 입력이 유효한 값이 아닌 경우
            #사용자가 입력한 데이터를 바탕으로 생성된 form개게와 error변수를 HTML파일에 전달
            return render(request, 'vote:cregister.html', {'f':form, 'error':'유효하지 않는 값입니다.'})
        
# Question 객체의 데이터를 사용자가 수정하는 뷰
@login_required
def qupdate(request, q_id):
    obj = get_object_or_404(Question, id = q_id)
    if request.method == "GET":
        #데이터베이스에 저장된 Question객체의 정보를 기반으로 모델폼 객체를 생성
        #HTML로 변환시 빈칸이 아닌 값이 채워진 형태로 변환됨
        form = QuestionForm(instance = obj)
        return render(request, "vote/qupdate.html", {'f':form})
    elif request.method == "POST":
        #기존 객체에 저장된 변수값을 사용자의 입력데이터로 변경한 모델폼 객체를 생성
        form = QuestionForm(data = request.POST, instance = obj)
        if form.is_valid():#수정한 값이 유효한 값인지 확인
            #사용자가 입력한 데이터를 바탕으로 데이터베이스에 수정사항을 반영
            q = form.save()
            print('obj : ', obj)
            print('q : ', q)
            return HttpResponseRedirect(reverse('vote:index'))

# Choice 객체를 사용자가 수정하는 뷰
@login_required
def cupdate(request, c_id):
    c = get_object_or_404(Choice, id=c_id)
    if request.method == "GET":
        form = ChoiceForm(instance = c)
        return render(request, 'vote/cupdate.html', {'f':form})
    if request.method == "POST":
        form = ChoiceForm(data = request.POST, instance = c)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,)))
        else:
            pass
# Question 객체 삭제요청 처리 뷰
@login_required
def qdelete(request, q_id):
    #삭제할 객체를 찾기
    q = get_object_or_404(Question, id = q_id)
    #해당 객체를 데이터베이스에서 삭제함. 삭제한 객체에 저장된 변수값은 사용할 수 있음
    q.delete()
    return HttpResponseRedirect(reverse('vote:index'))
# Choice 객체 삭제요청 처리 뷰
# 1)매개변수를 추가(삭제하고자 하는 Choice객체의 id값)
@login_required
def cdelete(request, c_id):
    #2)매개변수로 Choice 객체 찾기
    c = get_object_or_404(Choice, id = c_id)
    c.delete()
    return HttpResponseRedirect(reverse('vote:detail', args=(c.q.id,)))
    #3)해당 객체 찾기
    #4)index나 detail의 URL을 전달
#5)vote폴더에 있는 urls.py에 뷰함수 등록    