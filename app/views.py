from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

MAX_ELEMENTS_IN_PAGE = 10


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', MAX_ELEMENTS_IN_PAGE))
    except ValueError:
        limit = MAX_ELEMENTS_IN_PAGE
    if limit > 100:
        limit = MAX_ELEMENTS_IN_PAGE
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


# можно еще всех страниц количество выводить
def new_questions(request):
    questions = Question.objects.new_questions()
    tags = Tag.objects.all()
    names = User.objects.all()
    page = paginate(request, questions)
    return render(request, 'new_questions.html', {
        'questions': page.object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def hot_questions(request):
    questions = Question.objects.hot_questions()
    tags = Tag.objects.all()
    names = User.objects.all()

    page = paginate(request, questions)
    return render(request, 'hot_questions.html', {
        'questions': page.object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def tag_news(request, tag_type):
    questions = Question.objects.questions_by_tag(tag_type)
    tags = Tag.objects.all()
    names = User.objects.all()

    page = paginate(request, questions)
    return render(request, 'tag_page.html', {
        'tag': tag_type,
        'questions': page.object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def question_page(request, question_id=0):
    question = get_object_or_404(Question, id=question_id)
    tags = Tag.objects.all()
    names = User.objects.all()

    return render(request, 'question_page.html', {
        'question': question,
        'tags': tags,
        'names': names,
    })


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('/')  # todo normal urls with params
            else:
                form.add_error(None, "Wrong pair login and password")
    try:
        tags = Tag.objects.all()
        names = User.objects.all()
    except ...:
        raise Http404
    context = {'form': form, 'tags': tags,
               'names': names, }
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('new_questions')


def sign_up_page(request):
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('new_questions')
    try:
        tags = Tag.objects.all()
        names = User.objects.all()
    except ...:
        raise Http404
    return render(request, 'sign_up.html', {
        'form': form,
        'tags': tags,
        'names': names,
    })


@login_required
def new_question(request):
    if request.method == 'GET':
        form = QuestionForm(request.user)
    else:
        form = QuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('question', question.pk)

    try:
        tags = Tag.objects.all()
        names = User.objects.all()
    except ...:
        raise Http404
    return render(request, 'new_question.html', {
        'form': form,
        'tags': tags,
        'names': names,
    })
