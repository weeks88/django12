from django.contrib import admin
#같은 폴더에 있는 models.py 접근해 정의된 모델클래스를 사용할 수 있도록 설정
from .models import *

admin.site.register(Post)
admin.site.register(PostType)
admin.site.register(PostImage)
admin.site.register(PostFile)
# Register your models here.
