import json
import math

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile
from django.template.defaulttags import register
from app.forms import LoginForm, SignUpForm, AnswerForm, UserForm, QuestionForm
from django.contrib.auth import logout, update_session_auth_hash


# Create your views here.

def pagination(request, listing, n):
    paginator = Paginator(listing, n)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


@register.filter
def intersection(queryset1,queryset2):
    return queryset1 & queryset2


def index(request):
    questions = Question.objects.all()[:100]
    content = pagination(request, questions, 10)
    return render(request, "index.html", context={'post': content})


def hot(request):
    questions = Question.objects.hot_que()[:100]
    content = pagination(request, questions, 10)
    return render(request, "hot.html", context={'post': content})

def tag(request, ind_que):
    questions = Question.objects.filter(tag__tag_title=Tag.objects.get(id=ind_que))
    if questions.exists():
        content = pagination(request, questions, 5)
        return render(request, "tags.html", {'title': Tag.objects.get(id=ind_que), 'post': content})
    else:
        raise Http404("Tag does not exist")


def question(request, ind_que):
    answers = Answer.objects.filter(que_id=ind_que)
    main_que = Question.objects.get(id=ind_que)
    content = pagination(request, answers, 5)
    if request.method == "GET":
        form = AnswerForm()
    elif request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('answer')
            ans_create = Answer(text_ans=text, author=Profile.objects.get(user=request.user),
                                que=Question.objects.get(id=ind_que))
            ans_create.save()
            if Answer.objects.filter(que_id=ind_que).count() < 5:
                return redirect('{}#{anchor}'.format(reverse("question", args=[ind_que]), anchor=ans_create.id))
            else:
                result_page = math.ceil(Answer.objects.count_answ(ind_que) / 5)
                return redirect('{}?page={page}#{anchor}'.format(reverse("question", args=[ind_que]), page=result_page,
                                                                 anchor=ans_create.id))
    return render(request, "question.html", {'form': form, 'post': content, 'que': main_que})


contin = 1


def login_(request):
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
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                form.add_error(None, "User is already registered. Please, login")
            else:
                if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                    form.add_error(None, "Passwords doesn`t match!")
                else:
                    user_create = User.objects.create_user(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'), email=form.cleaned_data.get('email'))
                    profile_create = Profile(user=user_create)
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
            que_create = Question(title=form.cleaned_data.get('title'), text_que=form.cleaned_data.get('text'), author=Profile.objects.get(user=request.user))
            que_create.save()
            tags = form.cleaned_data['tag'].split(', ')

            for tag in tags:
                t = Tag.objects.filter(tag_title=tag)
                if t.exists():
                    que_create.tag.add(Tag.objects.get(tag_title=tag))
                else:
                    new_tag = Tag(tag_title=tag)
                    new_tag.save()
                    que_create.tag.add(new_tag)
            return redirect(reverse('question', args=[que_create.id]))
            # return redirect(reverse('index'))
    return render(request, "ask.html", {'form': form})


@login_required()
def settings(request):
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = UserForm(initial=initial_data)
    elif request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            redirect(reverse('settings'))
    else:
        messages.error(request, 'Please correct the error below.')
    return render(request, "settings.html", {'form': form})

# @login_required()
# def logout_view(request):
#     auth.logout(request)
@login_required()
@require_POST
def vote(request):
    question_id = request.POST['id']
    type = request.POST.get('type')
    q = Question.objects.get(id=question_id)
    if type == 'like':
        new_like = LikeToQue.objects.create(person_like_que=request.user.profile, like_que=q, is_like=True)
        new_like.save()
        q.rating += 1
        q.save()
    if type == 'dislike':
        new_like = LikeToQue.objects.create(person_like_que=request.user.profile, like_que=q, is_like=False)
        new_like.save()
        q.rating -= 1
        q.save()
    response = {
        'rating': q.rating,
        'id':q.id
    }
    return JsonResponse(response)

@login_required()
@require_POST
def correct_answer(request):
    if request.method == 'POST':
        answer_id = request.POST['id']
        type = request.POST.get('type')
        answer = Answer.objects.get(id=answer_id)
        if type == 'correct':
            answer.is_correct = True
            answer.save()
        if type == 'uncorrect':
            answer.is_correct = False
            answer.save()
    return JsonResponse({})

