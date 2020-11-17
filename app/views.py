from django.shortcuts import render

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
    'tags': ['taag1', 'tag2', 'tagn', ],
    'answers': [{'text': 'first answer!!!!!',
                 'id': 0,
                 'rating': -4, } for i in range(15)]})

tags = [f'tag{idx}' for idx in range(10)]
names = [f'name{idx}' for idx in range(10)]


def new_questions(request):
    # object_list = questions
    # paginator = Paginator(object_list, 5)
    # page = request.GET.get('page')
    # try :
    #     questions_list = paginator.page(page)
    # except PageNotAnInteger:
    #     questions_list = paginator.page(1)
    # except EmptyPage:
    #     questions_list = paginator.page(paginator.num_pages)
    return render(request, 'new_questions.html', {
        'questions': questions,
        'page': 0,
        'tags': tags,
        'names': names,
    })


def hot_questions(request):
    return render(request, 'hot_questions.html', {
        'questions': questions,
        'tags': tags,
        'names': names,
    })


def tag_news(request, tag_type):
    return render(request, 'tag_page.html', {
        'tag' : tag_type,
        'questions': questions,
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
