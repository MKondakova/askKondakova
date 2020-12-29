from django.core.management.base import BaseCommand, CommandError
from app.models import Question, User, Tag, Answer
from faker import Faker
from random import choice

f = Faker()


class Command(BaseCommand):
    help = 'Enter database size: small, medium or large'

    def handle(self, *args, **options):
        self.fill_users(10)
        self.fill_tags(10)
        self.fill_questions(40)
        self.fill_answers(100)

    def fill_tags(self, count):
        for i in range(count):
            Tag.objects.create(name=f.word())

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
        for i in range(count):
            User.objects.create_user(username=f.user_name(), email=f.email())

    def fill_answers(self, count):
        question_ids = list(
            Question.objects.values_list('id', flat=True)
        )
        author_ids = list(
            User.objects.values_list('id', flat=True)
        )

        for i in range(count):
            Answer.objects.create(
                author_id=choice(author_ids),
                question_id=choice(question_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            )

