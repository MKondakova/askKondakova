from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Question, Answer, User, Profile, Tag, MAX_TITLE_LENGTH, MAX_TAG_LENGTH, MAX_NICKNAME_LENGTH, \
    MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, MAX_TAGS_PER_QUESTION, QuestionVote, AnswerVote


class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH)
    password = forms.CharField(widget=forms.PasswordInput, max_length=MAX_PASSWORD_LENGTH)


class RegistrationForm(forms.ModelForm):
    nickname = forms.CharField(max_length=MAX_NICKNAME_LENGTH)
    password = forms.CharField(widget=forms.PasswordInput, max_length=MAX_PASSWORD_LENGTH)
    repeat_password = forms.CharField(widget=forms.PasswordInput, max_length=MAX_PASSWORD_LENGTH)
    avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        user = User(username=self.cleaned_data.get('username'), email=self.cleaned_data.get('email'))
        user.set_password(self.cleaned_data.get('password'))
        profile = Profile(nickname=self.cleaned_data.get('nickname'), user=user)

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
    tags = forms.CharField(
        help_text='Enter tags with whitespaces. Length of tag must be less then %s symbols' % MAX_TAG_LENGTH,
        required=False)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags = tags.split()
        if len(tags) > MAX_TAGS_PER_QUESTION:
            raise ValidationError('Too many tags. Use no more then %(value)s tags',
                                  params={'value': MAX_TAGS_PER_QUESTION})
        is_correct = all((lambda tag: len(tag) <= MAX_TAG_LENGTH) for tag in tags)
        if not is_correct:
            raise ValidationError('One of tags too long')
        return tags

    def save(self, commit=True):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'], author=self._user)
        if commit:
            question.save()
            with transaction.atomic():
                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in self.cleaned_data['tags']]
            question.tags.set(tags)
        return question

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
        fields = ['nickname', 'avatar']


class VoteForm(forms.Form):
    action = forms.CharField(max_length=8)
    object_type = forms.CharField(max_length=9)
    rate_object_id = forms.IntegerField(min_value=0)

    def __init__(self, user_id, *args, **kwargs):
        self._user_id = user_id
        super(VoteForm, self).__init__(*args, **kwargs)


    def clean_object_type(self):
        object_type = self.cleaned_data.get('object_type')
        if not (object_type == 'question' or object_type == 'answer'):
            raise ValidationError('Wrong type format')
        return object_type

    def clean_action(self):
        action = self.cleaned_data.get('action')
        if action == 'like' or action == 'dislike':
            action = True if action == 'like' else False
        else:
            raise ValidationError('Wrong action format')
        return action

    def save(self, commit=True):
        vote_model = QuestionVote if self.cleaned_data.get('object_type') == 'question' else AnswerVote
        rate_object_model = Question if self.cleaned_data.get('object_type') == 'question' else Answer
        vote_model.objects.set_or_change_vote(self._user_id, self.cleaned_data.get('rate_object_id'),
                                              self.cleaned_data.get('action'))
        rate_object = rate_object_model.objects.get(id=self.cleaned_data.get('rate_object_id'))
        if commit:
            rate_object.update_rating()
        return rate_object


class MakeCorrectForm(forms.Form):
    answer_id = forms.IntegerField(min_value=0)

    def save(self, commit=True):
        answer_id = self.cleaned_data.get('answer_id')
        try:
            current_answer = Answer.objects.get(id=answer_id)
            current_answer.is_correct = True
            if commit:
                current_answer.save()
        except Answer.DoesNotExist:
            current_answer = None
        return current_answer
