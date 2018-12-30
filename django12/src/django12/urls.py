"""django12 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bookmark.views import index, booklist, bookdetail
#include() : 하위 URLConf 파일을 추가할 때 사용하는 함수
#urlpatterns : URL과 뷰함수를 등록 및 관리하는 변수
#URL 등록시 path 함수를 이용해 urlpatterns의 요소를 추가
#path(URL주소(문자열), 호출할 뷰함수/클래스 이름)

# 웹서버 기본주소 : 127.0.0.1:8000/
urlpatterns = [
    #기본주소 + admin주소로 클라이트가 요청한 경우, admin폴더/site폴더/urls.py가 실행
    path('admin/', admin.site.urls),
    path('', index), #127.0.0.1:8000으로 클라이언트가 요청했을 때, index함수가 호출
    path('list/', booklist), #127.0.0.1:8000/list/ 로 클라이언트가 요청했을때, booklist함수가 호출 
    path('detail/<int:bookid>/', bookdetail), #127.0.0.1:8000/detail/숫자/ 로 요청시 bookdetail이 호출되고 숫자데이터는 bookid저장됨
    path('vote/', include('vote.urls')), #127.0.0.1:8000/vote/로 시작하는 모든 요청을 vote폴더의 urls.py에서 처리하도록 등록
    path('cl/', include('customlogin.urls')),
    #해당 어플리케이션의 app_name 변수에 저장된 문자열 대신 사용할 그룹이름을 
    #namespace 매개변수에 대입시키면 됨
    #127.0.0.1:8000/auth/
    path('auth/', include('social_django.urls', namespace='social')),
    path('blog/', include('blog.urls')),
]

from django.conf import settings #setting.py에 설정된 값을 가져오기 위함
from django.conf.urls.static import static #MEDIA_URL과 MEDIA_ROOT를 연동하기 위한 함수
#URL 주소와 실제 저장된 파일 경로를 매칭
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
