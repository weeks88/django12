from django.db import models

#카테고리
class PostType(models.Model):
    name=models.CharField('카테고리', max_length=20)
    def __str__(self):
        return self.name

from django.conf import settings
#글(제목, 글쓴이-외래키, 글내용, 작성일, 카테고리-외래키)
class Post(models.Model):
    #models.PROTECT : 연결된 객체가 삭제되는 것을 막아주는 기능
    #models.SET_NULL : 연결된 객체가 삭제되면 null값을 저장
    #models.SET_DEFAULT : 연결된 객체가 삭제되면 기본 설정된 객체와 연결
    #models.SET(연결할 객체) : 연결된 객체가 삭제되면 매개변수로 지정된 객체로 연결
    #models.CASCADE : 연결된 객체가 삭제되면 같이 삭제됨
    type = models.ForeignKey(PostType, on_delete=models.PROTECT)
    headline = models.CharField('제목', max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #models.TextField : 글자수 제한이 없는 문자열 공간
    #null(기본값  False) : 데이터베이스에 객체를 저장할 때 해당 변수값이 비어있어도 생성되도록 허용
    #blank(기본값 False) : 폼객체.is_valid(), 폼객체.as_p을 사용했을때 사용자가 입력하지 않아도 되도록 허용
    content = models.TextField('내용', null=True, blank=True)
    #auto_now_add : 객체가 생성될때 자동으로 서버의 현재시간을 저장하도록 설정
    pub_date=models.DateTimeField('작성일', auto_now_add=True)
    class Meta:
        ordering=['-id']
    
#이미지(글-외래키, 이미지파일)
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    image = models.ImageField('이미지 파일', upload_to='images/%Y/%m/%d')
    #imageField : 이미지가 저장된 경로를 저장하는 공간
    #upload_to :  실제 이미지를 저장할 때 사용할 경로
    # %Y : 해당서버의 현재 연도, %m : 해당서버의 현재 월, %d: 해당 서버의 현재일
    
    #객체 삭제시 호출되는 함수. 객체 삭제 전 실제 이미지파일을 삭제하는 코드를 삽입
    def delete(self, using=None, keep_parents=False):
        #image변수에 저장되있는 경로의 파일을 지우는 과정
        self.image.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)
    
#파일(글-외래키, 파일)
class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField('첨부파일', upload_to='files/%Y/%m/%d')
    #FileField : 파일(이미지, 실행파일, 워드, 액설 등)의 경로등을 저장하는 공간

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)