from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from askKondakova.settings import LOGIN_URL

MAX_ELEMENTS_IN_PAGE = 10
NUM_PAGE_LINKS = 5

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', MAX_ELEMENTS_IN_PAGE))
    except ValueError:
        limit = MAX_ELEMENTS_IN_PAGE
    if limit > MAX_ELEMENTS_IN_PAGE:
        limit = MAX_ELEMENTS_IN_PAGE
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    start_index = max(1, page_obj.number - NUM_PAGE_LINKS)
    end_index = min(paginator.num_pages, page_obj.number + NUM_PAGE_LINKS)

    page_links = [i for i in range(start_index, end_index + 1)]
    return {'page_obj': page_obj, 'page_links': page_links}


def new_questions(request):
    questions = Question.objects.new_questions()
    tags = Tag.objects.all()
    names = User.objects.all()[:10]
    page = paginate(request, questions)
    return render(request, 'new_questions.html', {
        'questions': page['page_obj'].object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def hot_questions(request):
    questions = Question.objects.hot_questions()
    tags = Tag.objects.all()
    names = User.objects.all()[:10]

    page = paginate(request, questions)
    return render(request, 'hot_questions.html', {
        'questions': page['page_obj'].object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def tag_news(request, tag_type):
    questions = Question.objects.questions_by_tag(tag_type)
    tags = Tag.objects.all()
    names = User.objects.all()[:10]

    page = paginate(request, questions)
    return render(request, 'tag_page.html', {
        'tag': tag_type,
        'questions': page['page_obj'].object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def question_page(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        form = AnswerForm(request.user, question_id)
    else:
        form = AnswerForm(request.user, question_id, request.POST)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('question', kwargs={'question_id': question_id}) + '#answer_' + str(answer.id))

    tags = Tag.objects.all()
    names = User.objects.all()[:10]

    return render(request, 'question_page.html', {
        'form': form,
        'question': question,
        'tags': tags,
        'names': names,
    })


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        request.session['next_url'] = request.GET.get('next', '/')
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.session.pop('next_url', '/'))
            else:
                form.add_error(None, "Wrong pair login and password")
    try:
        tags = Tag.objects.all()
        names = User.objects.all()[:10]
    except ...:
        raise Http404
    context = {'form': form, 'tags': tags,
               'names': names, }
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('new_questions')


@login_required
def settings_page(request):
    if request.method == 'GET':
        form = SettingsForm(instance=request.user.profile)
    else:
        form = SettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
    try:
        tags = Tag.objects.all()[:20]
        names = User.objects.all()[:10]
    except ...:
        raise Http404
    return render(request, 'settings.html', {
        'form': form,
        'tags': tags,
        'names': names,
    })


def sign_up_page(request):
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('new_questions')
    try:
        tags = Tag.objects.all()
        names = User.objects.all()[:10]
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
        names = User.objects.all()[:10]
    except ...:
        raise Http404
    return render(request, 'new_question.html', {
        'form': form,
        'tags': tags,
        'names': names,
    })


@require_POST
def make_correct(request):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': request.build_absolute_uri(LOGIN_URL)})
    form = MakeCorrectForm(request.POST)
    if form.is_valid():
        form.save()
    return JsonResponse({})


@require_POST
def vote(request):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': request.build_absolute_uri(LOGIN_URL)})
    form = VoteForm(request.user.id, request.POST)
    if form.is_valid():
        rate_object = form.save()
        return JsonResponse({'qrating': rate_object.rating})
    else:
        print(form.errors)
        return JsonResponse(status=400, data={'Wrong format'})
