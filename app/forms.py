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

    def save(self, commit=True):
        user = User(self.cleaned_data.get('username'), self.cleaned_data.get('email'),
                    self.cleaned_data.get('password'), )
        profile = Profile(nick_name=self.cleaned_data.get('nick_name'), user=user)
        if self.cleaned_data.get('avatar') is not None:
            profile.avatar = self.cleaned_data.get('avatar')
        if commit:
            user.save()
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

    def save(self, commit=True):
        self.cleaned_data['author'] = self._user
        if commit:
            return Question.objects.create(**self.cleaned_data)
        return Question(**self.cleaned_data)

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    def __init__(self, user, question_id, *args, **kwargs):
        self._user = user
        self._question_id = question_id
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.question_id = self._question_id
        if commit:
            answer.save()
        return answer

    class Meta:
        model = Answer
        fields = ['text']


class SettingsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(SettingsForm, self).__init__(*args, **kwargs)
        if instance:
            email = instance.user.email
            self.fields["email"].initial = email

    def save(self, commit=True):
        profile = super(SettingsForm, self).save(commit)
        if commit and self.has_changed() and 'email' in self.changed_data:
            user = self.instance.user
            user.email = self.cleaned_data.get('email')
            user.save()
        return profile

    class Meta:
        model = Profile
        fields = ['nick_name', 'avatar']
