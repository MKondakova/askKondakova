from django.db import models
from django.contrib.auth.models import User

MAX_TITLE_LENGTH = 50
MAX_TAG_LENGTH = 30
MAX_NICK_NAME_LENGTH = 30
MAX_USERNAME_LENGTH = 150
MAX_PASSWORD_LENGTH = 128
MAX_TAGS_PER_QUESTION = 10


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', default='avatars/default_pic.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=MAX_NICK_NAME_LENGTH)


class Tag(models.Model):
    name = models.CharField(max_length=MAX_TAG_LENGTH, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-added_at')

    def hot_questions(self):
        return self.order_by('-rating')

    def questions_by_tag(self, tag):
        return self.filter(tags__name__contains=tag)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['added_at']),
            models.Index(fields=['rating'])
        ]


class Question(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH, verbose_name='Заголовок')  # todo 50?
    text = models.TextField(verbose_name='Текст')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    correctAnswer = models.BooleanField(default=False)

    objects = QuestionManager()

    def answer_count(self):
        return self.answers.count()

    def __str__(self):
        return self.title + " " + self.author.__str__()


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('added_at')


class Answer(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    objects = AnswerManager()

    def __str__(self):
        return self.author.username + " " + self.added_at.__str__()


class VoteManager(models.Manager):
    def get_likes(self, primary_key):
        return self.filter(rate_object=primary_key, isLike=True).count()

    def get_dislikes(self, primary_key):
        return self.filter(rate_object=primary_key, isLike=False).count()

    def get_rating(self, primary_key):
        return self.get_likes(primary_key) - self.get_dislikes(primary_key)


class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLike = models.BooleanField()
    rate_object = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = VoteManager


class AnswerVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isLike = models.BooleanField()
    rate_object = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = VoteManager

