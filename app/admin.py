from django.contrib import admin

# Register your models here.
from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile


# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)

admin.site.register(Answer)
admin.site.register(LikeToAns)
admin.site.register(LikeToQue)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Profile)