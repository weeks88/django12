from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

#제네릭 뷰 : 장고에서 제공하는 여러가지 뷰 기능을 수행하는 클래스
#뷰클래스 구현시 제네릭뷰를 상속받아서 변수/메소드를 수정해 그 기능을 사용할 수 있음
#ListView : 특정 모델클래스의 객체의 목록을 다루는 기능을 수행하는 제네릭 뷰
#DetailView : 특정 모델클래스의 객체 한개를 템플릿에 전달할 때 사용하는 제네릭 뷰

#% 제네릭뷰 사용시 문서를 확인해 어떤 변수/메소드를 수정할 수 있는지 파악해야 함.
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
#게시물 목록(index)
class Index(ListView):
    template_name='blog/index.html' #HTML파일의 경로를 저장하는 변수
    model= Post #목록으로 보여질 모델클래스를 지정하는 변수
    context_object_name='post_list' #템플릿에게 객체 리스트를 넘겨줄때 사용할 키값
    paginate_by=5 #한페이지에 몇개의 객체를 보여줄지 설정

#상세페이지(detail)
class Detail(DetailView):
    template_name='blog/detail.html'
    model=Post
    context_object_name='obj'
    
#FormView : 폼클래스를 객체로 생성해 템플릿으로 넘겨주는 뷰
from .forms import *
#글 등록 페이지(postRegister)
class PostRegister(LoginRequiredMixin, FormView):
    template_name = 'blog/postregister.html'
    form_class = PostForm
    context_object_name = 'form'
    
    #is_valid()함수가 True를 반환했을때에 대한 처리를  form_valid()함수를 오버라이딩해서 구현
    def form_valid(self, form):
        #사용자 입력에 대한 객체 생성 처리
        #author변수에 값이 채워져 있지 않으므로 데이터베이스 저장하지 않고 변환만 함
        obj = form.save(commit=False) #obj:Post 객체(데이터베이스 저장x)
        #뷰 함수의 request 매개변수를 뷰클래스에서 사용할 때 self.request로 사용 가능
        #request.user : 요청한 클라이언트의 로그인 정보(User 모델클래스의 객체)
        obj.author = self.request.user #글쓴이 정보 채우기
        obj.save()         #데이터베이스에 Post객체 저장
        
        #사용자가 업로드한 이미지, 파일을 데이터베이스에 객체로 저장
        #request.FIELS : 클라이언트가 서버로 보낸 파일정보를 관리하는 변수
        for f in self.request.FILES.getlist('images'):
            # f : 이미지 정보. f를 이용해 PostImage 객체를 생성, 데이터베이스에 저장
            # 객체 생성시 각 변수에 값을 채워서 생성할 수 있음
            image = PostImage(post = obj, image = f)
            #image = PostImage()
            #image.post = obj
            #image.image = f
            image.save() #데이터베이스에 새로운 PostImage객체가 저장됨
        
        for f in self.request.FILES.getlist('files'):
            file = PostFile(post = obj, file = f)
            file.save()
        
        #만들어진 Post객체의 id값을 detail 뷰에 넘겨주면서 마무리    
        return HttpResponseRedirect( reverse('blog:detail', args=(obj.id,)))
    
#검색기능을 구현한 뷰클래스(searchP)
class SearchP(FormView):
    template_name = 'blog/searchP.html'
    form_class = SearchForm
    context_object_name = 'form'
    
    #유효성 검사를 통과한 요청들을 처리하기 위해 form_valid함수 오버라이딩
    def form_valid(self, form):
        #Post 객체 중에 사용자가 입력한 텍스트를 포함한 객체를 찾아 HTML결과로 보여주기
        #사용자가 입력한 텍스트 추출
        search_word = form.cleaned_data['search_word']
        #추출된 텍스트를 포함한 Post객체들을 추출(제목 검색. post객체의 headline변수)
        #Post.objects.filter(변수__필터링 = 값)
        #변수와 값을 필터링 조건에 맞춰서 비교후 만족하는 객체를 추출하는 함수
        #contains : 해당변수가 우변값을 포함한 경우를 추출하겠다는 설정
        post_list = Post.objects.filter(headline__contains=search_word)
        #추출된 결과를 HTML로 전달(검색결과+재검색할 수 있는 입력공간+검색어)
        return render(self.request, self.template_name, {'form' : form, 'search_word' : search_word, 'postlist' : post_list})
    