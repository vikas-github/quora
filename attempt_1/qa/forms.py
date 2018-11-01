from django import forms
from .models import Question, Answer


class PostAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('answer_text',)
