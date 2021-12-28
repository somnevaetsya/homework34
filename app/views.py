import math

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile
from django.template.defaulttags import register
from app.forms import LoginForm, SignUpForm, AnswerForm, UserForm, QuestionForm
from django.contrib.auth import logout, update_session_auth_hash


# Create your views here.
# Не работает вход, потому запись идет в обычном тексте,а не в хеше //done
# Проверить, создается ли тег при создании вопроса // done
# Реализовать нормальный выход из профиля //done
# Реализовать переход на страницу вопроса после его создания //done
# Реализовать continue в login //done
# Реализовать переход на страницу с ответом после написания ответа
# Посмотреть фильтр подсчета лайков, потому что неправильно считает 


@register.filter
def get_item(dictionary, key):
    return dictionary[0][key]


def pagination(request, listing, n):
    paginator = Paginator(listing, n)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    questions = [{'title': Question.objects.new_que()[i].title,
                  'text': Question.objects.new_que()[i].text_que,
                  'answer': Answer.objects.count_answ(Question.objects.new_que()[i].id),
                  'like_to_que': LikeToQue.objects.count_like_que(Question.objects.new_que()[i].id),
                  'tag': Question.objects.get_tag(Question.objects.new_que()[i].id, 0),
                  'id': Question.objects.new_que()[i].id}
                 # 'url': Question.objects.get(id=i).get_absolute_url()}
                 for i in range(0, 100)
                 ]
    content = pagination(request, questions, 10)
    return render(request, "index.html", context={'post': content})


def hot(request):
    questions = [{'title': Question.objects.hot_que(i).title,
                  'text': Question.objects.hot_que(i).text_que,
                  'tag': Question.objects.get_tag(Question.objects.hot_que(i).id, 0),
                  'answer': Answer.objects.count_answ(Question.objects.hot_que(i).id),
                  'like_to_que': LikeToQue.objects.count_like_que(Question.objects.hot_que(i).id),
                  'tag': Question.objects.get_tag(Question.objects.hot_que(i).id, 0),
                  'id': Question.objects.hot_que(i).id}
                 # 'url': Question.objects.get(id=i).get_absolute_url()}
                 for i in range(0, Question.objects.count())
                 ]
    content = pagination(request, questions, 10)
    return render(request, "hot.html", context={'post': content})


# questions = [
#     {
#         "title": f"Title {i}",
#         "id": i,
#         "text": f"This is text for {i} question.",
#     } for i in range(20)
# ]

def tag(request, ind_que):
    cur_tag = Question.objects.get_tag(ind_que, 0)
    ques = Question.objects.get_que_tag(cur_tag)
    if ques.exists():
        questions = [{'title': Question.objects.get_que_tag(cur_tag)[i].title,
                      'text': Question.objects.get_que_tag(cur_tag)[i].text_que,
                      'answer': Answer.objects.count_answ(Question.objects.get_que_tag(cur_tag)[i].id),
                      'tag': Question.objects.get_tag(Question.objects.get_que_tag(cur_tag)[i].id, 0),
                      'like_to_que': LikeToQue.objects.count_like_que(Question.objects.get_que_tag(cur_tag)[i].id),
                      'id': ind_que}
                     # 'url': Question.objects.get(id=i).get_absolute_url()}
                     for i in range(Tag.objects.count_tags(cur_tag))
                     ]
        content = pagination(request, questions, 5)
        return render(request, "tags.html", {'post': content})
    else:
        raise Http404("Tag does not exist")


def question(request, ind_que):
    answers = [{
        'text_ans': Answer.objects.get_answer(ind_que, i - 1),
        'like_to_ans': LikeToAns.objects.count_like_ans(i),
        'id': Answer.objects.get_answer(ind_que, i - 1).id,
    }
        # 'url': Question.objects.get(id=i).get_absolute_url()}
        for i in range(1, Answer.objects.count_answ(ind_que) + 1)
    ]
    main_que = {'title': Question.objects.get(id=ind_que).title,
                'text': Question.objects.get(id=ind_que).text_que,
                'like_to_que': LikeToQue.objects.count_like_que(ind_que),
                'tag': Question.objects.get_tag(ind_que, 0),
                'id': ind_que}
    content = pagination(request, answers, 5)
    if request.method == "GET":
        form = AnswerForm()
    elif request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('answer')
            ans_create = Answer(text_ans=text, person_ans=Profile.objects.get(user=request.user),
                                que=Question.objects.get(id=ind_que))
            ans_create.save()
            like_ans_create = LikeToAns(like_ans=ans_create, person_like_ans=Profile.objects.get(user=request.user))
            like_ans_create.save()
            if Answer.objects.count_answ(ind_que) < 5:
                return redirect('{}#{anchor}'.format(reverse("question", args=[ind_que]), anchor=ans_create.id))
            else:
                result_page = math.ceil(Answer.objects.count_answ(ind_que) / 5)
                return redirect('{}?page={page}#{anchor}'.format(reverse("question", args=[ind_que]), page=result_page,
                                                                 anchor=ans_create.id))
    return render(request, "question.html", {'form': form, 'post': content, 'que': main_que})


contin = 1


def login_(request):
    print(request.POST)
    global contin
    if request.method == 'GET':
        form = LoginForm()
        contin = request.META['HTTP_REFERER']
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Incorrect login or password")
            else:
                auth.login(request, user)
                return redirect(contin)
    return render(request, "login.html", {'form': form})


def signup(request):
    print(request.POST)
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            if User.objects.filter(username=name).exists():
                form.add_error(None, "User is already registered. Please, login")
            else:
                name = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user_create = User.objects.create_user(username=name, password=raw_password)
                profile_create = Profile.objects.create(user=user_create)
                profile_create.save()
                auth.login(request, user_create)
                return redirect(reverse('index'))
    return render(request, "sign_up.html", {'form': form})


@login_required()
def ask(request):
    if request.method == 'GET':
        form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            que_title = form.cleaned_data.get('title')
            que_text = form.cleaned_data.get('text')
            que_tag = form.cleaned_data.get('tag')
            que_create = Question(title=que_title, text_que=que_text, person_que=Profile.objects.get(user=request.user))
            que_create.save()
            tag_create = Tag.objects.create(tag_title=que_tag, rating=0)
            tag_create.save()
            que_create.tag.add(tag_create)
            que_create.save()
            return redirect(reverse('question', args=[que_create.id]))
            # return redirect(reverse('index'))
    return render(request, "ask.html", {'form': form})


@login_required()
def settings(request):
    if request.method == 'GET':
        form = UserForm(data={'username': request.user.username, 'email': request.user.email})
    elif request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            print(name)
            to_change = User.objects.get(username__exact=name)
            to_change.email = mail
            to_change.set_password(form.cleaned_data.get('password_repeat'))
            to_change.save()
            update_session_auth_hash(request, to_change)
    else:
        messages.error(request, 'Please correct the error below.')
    return render(request, "settings.html", {'form': form})

# @login_required()
# def logout_view(request):
#     auth.logout(request)
