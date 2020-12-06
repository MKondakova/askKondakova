from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render

MAX_ELEMENTS_IN_PAGE = 10
questions = [
    {
        'title': f'title {idx}',
        'id': idx,
        'text': ('some text' * 4 * (idx + 1)),
        'rating': idx % 3,
        'answer_count': 7,
        'tags': ['taag1', 'tag2', 'tagn', ],
        'answers': [
            {'text': 'first answer!!!!!',
             'id': 0,
             'rating': -4, },
            {'text': 'just reboot',
             'id': 4,
             'rating': 5, },
        ],
    } for idx in range(10)
]
questions.append({
    'title': 'Nice new title',
    'id': 10,
    'text': ('some text' * 50),
    'rating': 2312,
    'answer_count': 0,
    'tags': ['taag1', 'tag2', 'tagn', ],
    'answers': []})

questions.append({
    'title': 'Nice new title',
    'id': 11,
    'text': ('some text' * 50),
    'rating': 2312,
    'answer_count': 0,
    'tags': ['tag1', 'tag2', 'tagn', ],
    'answers': [{'text': 'first answer!!!!!',
                 'id': 0,
                 'rating': -4, } for i in range(15)]})

tags = [f'tag{idx}' for idx in range(10)]
names = [f'name{idx}' for idx in range(10)]


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
    page = paginate(request, questions)
    return render(request, 'new_questions.html', {
        'questions': page.object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def hot_questions(request):
    page = paginate(request, questions)
    return render(request, 'hot_questions.html', {
        'questions': page.object_list,
        'page' : page,
        'tags': tags,
        'names': names,
    })


def tag_news(request, tag_type):
    page = paginate(request, list(filter(lambda question: (tags.count(tag_type) > 0), questions)))
    return render(request, 'tag_page.html', {
        'tag': tag_type,
        'questions': page.object_list,
        'page': page,
        'tags': tags,
        'names': names,
    })


def question_page(request, question_id=0):
    question = questions[question_id]
    return render(request, 'question_page.html', {
        'question': question,
        'tags': tags,
        'names': names,
    })


def login_page(request):
    return render(request, 'login.html', {
        'tags': tags,
        'names': names,
    })


def signup_page(request):
    return render(request, 'sign_up.html', {
        'tags': tags,
        'names': names,
    })


def new_question(request):
    return render(request, 'new_question.html', {
        'tags': tags,
        'names': names,
    })
