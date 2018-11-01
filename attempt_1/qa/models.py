from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_bio = models.CharField(max_length=70, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.SmallIntegerField(null=True, blank=True)
    profile_cred = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    studied = models.CharField(max_length=50, blank=True)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    q_pub_date = models.DateTimeField('Date Question Published')
    q_modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer_text = models.TextField(max_length=5000)
    answer_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ans_auth')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    a_pub_date = models.DateTimeField('Date Answer Published')
    a_modified_date = models.DateTimeField('Date Answer Modified', null=True, blank=True)

    def __str__(self):
        return self.answer_text


class VoteAnswerMod(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # 1=Upvote, 0=Downvote
    action_taken = models.SmallIntegerField()
    vote_user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_date = models.DateTimeField('Date Upvoted')

    def __str__(self):
        return self.answer.answer_text


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=2000, null=True, blank=True)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField('Date Commented')


class BookmarkAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    b_user = models.ForeignKey(User, on_delete=models.CASCADE)
    b_date = models.DateTimeField('Bookmark Date')


class TopicStore(models.Model):
    topic_text = models.CharField(max_length=70, blank=False)
    topic_dp = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.topic_text


class QuestionTopic(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicStore, on_delete=models.CASCADE)


class FollowTopic(models.Model):
    f_user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicStore, on_delete=models.CASCADE)
    f_date = models.DateTimeField('Follow Date')


class BookTopic(models.Model):
    b_user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(TopicStore, on_delete=models.CASCADE)
    b_date = models.DateTimeField('Bookmark Date')


class FollowQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    f_user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_date = models.DateTimeField('Follow Date')
