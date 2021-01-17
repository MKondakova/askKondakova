from django.core.management.base import BaseCommand, CommandError
from app.models import Question, User, Tag, Answer, QuestionVote, AnswerVote, Profile
from faker import Faker
from random import choice

f = Faker()

quantity_values = {
    'small': {
        'questions': 50,
        'answers': 100,
        'tags': 30,
        'users': 10,
        'question_likes': 100,
        'answer_likes': 50,
    },
    'medium': {
        'questions': 100,
        'answers': 300,
        'tags': 100,
        'users': 50,
        'question_likes': 500,
        'answer_likes': 250,

    },
    'large': {
        'questions': 1000,
        'answers': 2000,
        'tags': 500,
        'users': 500,
        'question_likes': 8000,
        'answer_likes': 1700,
    }
}


class Command(BaseCommand):
    help = 'Enter database size: small, medium or large'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--size',
            nargs='?',
            type=str,
            action='store',
            choices=[
                'small',
                'medium',
                'large',
            ],
            default='small'
        )

    def handle(self, *args, **options):
        quantity = quantity_values[options['size']]
        self.fill_users(quantity['users'])
        self.fill_tags(quantity['tags'])
        self.fill_questions(quantity['questions'])
        self.fill_answers(quantity['answers'])
        self.fill_question_likes(quantity['question_likes'])
        self.fill_answer_likes(quantity['answer_likes'])

    def fill_tags(self, count):
        names = f.words(nb=count, unique=True)
        for i in range(count):
            Tag.objects.create(name=names[i])

    def fill_questions(self, count):
        author_ids = list(
            User.objects.values_list('id', flat=True)
        )
        tags = list(
            Tag.objects.all()
        )
        for i in range(count):
            question = Question.objects.create(
                author_id=choice(author_ids),
                title=f.sentence()[:50],
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            )
            for j in range(f.random_int(min=1, max=3)):
                question.tags.add(choice(tags))

    def fill_users(self, count):
        avatars = ['avatars/bee.jpg', 'avatars/cat.jpg', 'avatars/tomato.png',
                   'avatars/unicorn.jpg', 'avatars/pigeon.jpeg', 'avatars/tiger.jpeg']
        for i in range(count):
            user = User.objects.create_user(username=f.unique.user_name(), email=f.email())
            Profile.objects.create(avatar=choice(avatars), user=user, nick_name=user.username)

    def fill_answers(self, count):
        question_ids = list(
            Question.objects.values_list('id', flat=True)
        )
        user_ids = list(
            User.objects.values_list('id', flat=True)
        )

        for i in range(count):
            Answer.objects.create(
                author_id=choice(user_ids),
                question_id=choice(question_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            )

    def fill_answer_likes(self, count):
        answer_ids = list(
            Answer.objects.values_list('id', flat=True)
        )
        user_ids = list(
            User.objects.values_list('id', flat=True)
        )
        for i in range(count):
            try:
                a = AnswerVote.objects.get(author_id=choice(user_ids),
                                           rate_object_id=choice(answer_ids), )
            except AnswerVote.DoesNotExist:
                a = AnswerVote(
                    author_id=choice(user_ids),
                    rate_object_id=choice(answer_ids),
                )
            a.is_like = choice([True, False])
            a.save()
        answers = Answer.objects.all()
        for i in answers:
            i.update_rating()

    def fill_question_likes(self, count):
        question_ids = list(
            Question.objects.values_list('id', flat=True)
        )
        user_ids = list(
            User.objects.values_list('id', flat=True)
        )
        for i in range(count):
            try:
                q = QuestionVote.objects.get(author_id=choice(user_ids),
                                             rate_object_id=choice(question_ids), )
            except QuestionVote.DoesNotExist:
                q = QuestionVote(
                    author_id=choice(user_ids),
                    rate_object_id=choice(question_ids),
                )
            q.is_like = choice([True, False])
            q.save()
        questions = Question.objects.all()
        for i in questions:
            i.update_rating()
