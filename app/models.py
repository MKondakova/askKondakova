from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-added_at')

    def hot_questions(self):
        return self.order_by('-rating')

    def questions_by_tag(self, tag):
        return self.filter(tags__contains='tag')


class Question(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')  # todo 50?
    text = models.TextField(verbose_name='Текст')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = QuestionManager()

    def __str__(self):
        return self.title + " " + self.author.__str__()
    # correctAnswer


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('added_at')


class Answer(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    objects = AnswerManager()

    def __str__(self):
        return self.author.username + " " + self.added_at.__str__()


class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLike = models.BooleanField
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLike = models.BooleanField
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
