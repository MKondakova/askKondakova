from django import forms
from .models import Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()



class QuestionForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class RegistrationForm(forms.Form): pass


class ProfileEditForm(forms.Form): pass
