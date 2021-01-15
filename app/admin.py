from django.contrib import admin
from .models import Question, Answer, Tag, Profile, QuestionVote, AnswerVote

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(QuestionVote)
admin.site.register(AnswerVote)
