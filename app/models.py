from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.urls import reverse
from django.db.models import Count


# Create your models here.
class QuestionManager(models.Manager):
    def new_que(self):  #сортируем по дате, чтобы найти свежие
        return self.order_by('-id')

    def hot_que(self): #считаем количество ответов на вопрос и сортируем, начиная с большего
        hot_questions = Question.objects.annotate(count=Count('answer')).order_by("-count")
        return hot_questions


class Tag(models.Model):
    tag_title = models.CharField(max_length=256)

    def __str__(self):
        return self.tag_title

    def get_edit_url(self):
        return reverse('tag', args=(self.pk,))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', default='')
    email = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='cat_s_papirosoy.jpg')

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    text_ans = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer', default='')
    que = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer', default='')
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text_ans


class Question(models.Model):
    title = models.CharField(max_length=256)
    text_que = models.TextField()
    tag = models.ManyToManyField(Tag, related_name='question')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='question', default='')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class LikeToAns(models.Model):
    like_ans = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="like_ans", default='')
    is_like = models.BooleanField(default=True)
    person_like_ans = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="like_ans", default='')

    def __str__(self):
        return str(self.like_ans.text_ans)


class LikeToQue(models.Model):
    like_que = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='like_que', default='')
    is_like = models.BooleanField(default=True)
    person_like_que = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="like_que", default='')

    def __str__(self):
        return str(self.like_que.title)

