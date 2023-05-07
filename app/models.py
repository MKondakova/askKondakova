from django.contrib.auth.models import User
from django.db import models

MAX_TITLE_LENGTH = 50
MAX_TAG_LENGTH = 30
MAX_NICKNAME_LENGTH = 30
MAX_USERNAME_LENGTH = 150
MAX_PASSWORD_LENGTH = 128
MAX_TAGS_PER_QUESTION = 10


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', default='avatars/default_pic.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=MAX_NICKNAME_LENGTH)


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

    objects = QuestionManager()

    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    def answer_count(self):
        return self.answers.count()

    def __str__(self):
        return self.title + " " + self.author.__str__()


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('added_at')

    def get_correct_answer(self, question_id):
        return self.filter(question_id=question_id, is_correct=True)


class Answer(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    objects = AnswerManager()
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_correct:
            try:
                temp = Answer.objects.get(question_id=self.question_id, is_correct=True)
                if self != temp:
                    temp.is_correct = False
                    temp.save()
            except Answer.DoesNotExist:
                pass
        super(Answer, self).save(*args, **kwargs)

    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()

    def __str__(self):
        return self.author.username + " " + self.added_at.__str__()


class VoteManager(models.Manager):
    def get_likes(self, primary_key):
        return self.filter(rate_object=primary_key, is_like=True).count()

    def get_dislikes(self, primary_key):
        return self.filter(rate_object=primary_key, is_like=False).count()

    def get_rating(self, primary_key):
        return self.get_likes(primary_key) - self.get_dislikes(primary_key)

    def set_or_change_vote(self, author_id, rate_object_id, is_like):
        try:
            q = self.get(author_id=author_id, rate_object_id=rate_object_id, )
            if q.is_like == is_like:
                q.delete()
            else:
                q.is_like = is_like
                q.save()
        except self.model.DoesNotExist:
            q = self.model(
                author_id=author_id,
                rate_object_id=rate_object_id,
                is_like=is_like,
            )
            q.save()


class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    rate_object = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes")
    objects = VoteManager()

    class Meta:
        unique_together = ['author', 'rate_object']


class AnswerVote(models.Model):
    objects = VoteManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    rate_object = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes")
