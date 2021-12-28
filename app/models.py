from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.urls import reverse
from django.db.models import Count


# Create your models here.
class QuestionManager(models.Manager):
    def new_que(self):  #сортируем по дате, чтобы найти свежие
        return self.all()[:100]

    def get_tag(self, index, i):   #по индексу определяет тэг
        tags = Question.objects.get(id=index).tag.all()
        return tags[i].tag_title

    def get_que_tag(self, title):
        ques = Question.objects.all()
        return ques.filter(tag__tag_title=title)

    def hot_que(self, i): #считаем количество ответов на вопрос и сортируем, начиная с большего
        hot_questions = Question.objects.annotate(count=Count('que')).order_by("-count")
        return hot_questions[i]


class AnswerManager(models.Manager):
    def count_answ(self, index): #посчитать ответы
        find_title = Question.objects.get(id=index).title
        return self.filter(que__title=find_title).count()

    def get_answer(self, index, i): #получить ответ по индексу
        find_title = Question.objects.get(id=index).title
        return Answer.objects.filter(que__title=find_title)[i]


class TagManager(models.Manager):
    def hot_tags(self): #лучшие теги
        return self.order_by("rating").reverse()[:10]

    def count_tags(self, tag): #посчитать теги
        return self.filter(tag_title=tag).count()



class ProfileManager(models.Manager):
    def best_profiles(self): #лучшие из лучших
        return Answer.objects.annotate(count=Count('person_ans')).order_by("-count")[:10]


class LikeToQueManager(models.Manager):
    def count_like_que(self, index): #посчитать количество лайков на вопрос
        find_title = Question.objects.get(id=index).title
        return self.filter(like_que__title=find_title).count()


class LikeToAnsManager(models.Manager):
    def count_like_ans(self, index): #количество лайков на ответ
        find_text = Answer.objects.get(id=index).text_ans
        return self.filter(like_ans__text_ans=find_text).count()


class Tag(models.Model):
    tag_title = models.CharField(max_length=256)
    rating = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return ' '.join([self.tag_title, str(self.rating)])

    def get_edit_url(self):
        return reverse('tag', args=(self.pk,))


class Profile(models.Model):
    avatar = models.ImageField(blank=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', default='')

    objects = ProfileManager()


    def __str__(self):
        return self.user.username


class Answer(models.Model):
    text_ans = models.TextField()
    person_ans = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person_ans', default='')
    que = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='que', default='')

    objects = AnswerManager()

    def __str__(self):
        return self.text_ans


class Question(models.Model):
    date = models.DateField(auto_now=True)
    title = models.CharField(max_length=256)
    text_que = models.TextField()
    tag = models.ManyToManyField(Tag, related_name='tag')
    person_que = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person_que', default='')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('question', args=[str(self.id)])


class LikeToAns(models.Model):
    like_ans = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="like_ans", default='')
    person_like_ans = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="person_like_ans", default='')

    objects = LikeToAnsManager()

    def __str__(self):
        return str(self.like_ans.text_ans)


class LikeToQue(models.Model):
    like_que = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='like_que', default='')
    person_like_que = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="person_like_que", default='')

    objects = LikeToQueManager()

    def __str__(self):
        return str(self.like_que.title)

