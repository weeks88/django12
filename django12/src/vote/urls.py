from django.urls import path
from .views import *

app_name='vote' #하위URL 파일의 그룹 이름
#path 함수를 이용해 url과 함수를 등록
#기본주소 : 127.0.0.1:8000/vote/
urlpatterns=[
    #127.0.0.1:8000/vote/ 주소로 요청해야 vote의 index함수가 호출됨
    path('', index, name='index'),
    # 127.0.0.1:8000/vote/숫자/
    path('<int:qid>/', detail, name='detail'),
    # 127.0.0.1:8000/vote/vote 'vote:vote'
    path('vote/', vote, name='vote'),
    
    path('result/<int:q_id>/', result, name="result"),
    # 127.0.0.1:8000/vote/qr/
    path('qr/', qregister, name='qregister'),
    
    path('qu/<int:q_id>/', qupdate, name='qupdate'),
    path('qd/<int:q_id>/', qdelete, name='qdelete'),
    path('cd/<int:c_id>/', cdelete, name='cdelete'),
    path('cr/', cregister, name='cregister'),
    path('cu/<int:c_id>/', cupdate, name='cupdate'),
    
    ]