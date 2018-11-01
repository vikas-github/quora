from django.contrib import admin
from .models import Question, Answer, UserProfile, VoteAnswerMod, AnswerComment, BookmarkAnswer, TopicStore, QuestionTopic, FollowTopic, BookTopic
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProfile)
admin.site.register(VoteAnswerMod)
admin.site.register(AnswerComment)
admin.site.register(BookmarkAnswer)
admin.site.register(TopicStore)
admin.site.register(QuestionTopic)
admin.site.register(FollowTopic)
admin.site.register(BookTopic)
