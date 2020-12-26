from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')  # todo 50?
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # correctAnswer


class Answer(models.Model):
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)


class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLike = models.BooleanField
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

# class AnswerVote(models.Model):
#     autor
#     isLike
#     answer
#     question
