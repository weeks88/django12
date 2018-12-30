from django.db import models

# Create your models here.
#질문을 저장하는 모델클래스 생성
#질문제목 생성일
class Question(models.Model):
    name = models.CharField('설문조사 제목',max_length=100)
    #DateTimeField : 날짜와 시간데이터를 저장하는 공간을 정의할 때 사용하는 클래스
    #DateField : 날짜 데이터만 저장하는 공간
    date = models.DateTimeField('생성일')
    def __str__(self):
        return self.name
#답변
#어떤 질문에 연결되었는지 답변내용 투표수
class Choice(models.Model):
    name = models.CharField('답변항목',max_length=50)
    #IntegerField : 정수값을 저장하는 공간
    votes = models.IntegerField('투표수',default=0)
    # ForeignKey(연결할 모델클래스) : ForeignKey 객체를 만든 클래스의 객체들이 연결한 모델클래스의 
    # 객체들이 연결한 모델클래스의 객체와 연결할 수 있는 설정
    q = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.q.name +"/"+self.name
    
    class Meta: #모델클래스에 정의된 변수들을 처리할 때 사용하는 클래스
        verbose_name = '답변항목'
        ordering = ['q']