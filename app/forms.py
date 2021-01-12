from django import forms
from django.core.exceptions import ValidationError
from .models import Question, Answer, User, Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    nick_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField()

    def save(self):
        user = User.objects.create_user(self.cleaned_data.get('username'), self.cleaned_data.get('email'),
                                        self.cleaned_data.get('password'), )
        profile = Profile.objects.create(nick_name=self.cleaned_data.get('nick_name'), user=user)
        if self.cleaned_data.get('avatar') is not None:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        if password != repeat_password:
            raise ValidationError("Entered passwords do not match")

    class Meta:
        model = User
        fields = ['email', 'username']


class QuestionForm(forms.ModelForm):
    # tags = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(QuestionForm, self).__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class ProfileEditForm(forms.Form): pass
