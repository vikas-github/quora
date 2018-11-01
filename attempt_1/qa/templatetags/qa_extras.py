from django import template
from ..models import Question, Answer, VoteAnswerMod, UserProfile, BookmarkAnswer, QuestionTopic, FollowTopic, BookTopic, FollowQuestion
from django.conf import settings

register = template.Library()


@register.filter(name='isupvoted')
def isupvoted(answer, user):
    counter = VoteAnswerMod.objects.filter(answer=answer, vote_user=user, action_taken=1).count()
    return str(counter)


@register.filter(name='isdownvoted')
def isdownvoted(answer, user):
    counter = VoteAnswerMod.objects.filter(answer=answer, vote_user=user, action_taken=0).count()
    return str(counter)


@register.filter(name='getupvotecount')
def getupvotecount(answer):
    counter = VoteAnswerMod.objects.filter(answer=answer, action_taken=1).count()
    return str(counter)


@register.filter(name='getdownvotecount')
def getdownvotecount(answer):
    counter = VoteAnswerMod.objects.filter(answer=answer, action_taken=0).count()
    return str(counter)


@register.filter(name='getuseravatar')
def getuseravatar(user):
    u = UserProfile.objects.get(user=user)
    if u.avatar:
        return u.avatar.url
    else:
        g = u.gender
        if g == 1:
            return 'static/images/avatars/users-2.png'
        elif g == 0:
            return 'static/images/avatars/users-3.png'
        else:
            return 'static/images/avatars/user_default.png'


@register.filter(name='getanswertoshow')
def getanswertoshow(question, pid):

    def safe_get_answer(aid):
        try:
            item = Answer.objects.get(pk=aid)
            return item
        except:
            return False

    if pid > 0:
        return safe_get_answer(pid)


@register.filter(name='isanswerbookmarked')
def isanswerbookmarked(answer, user):
    counter = BookmarkAnswer.objects.filter(answer=answer, b_user=user).count()
    return str(counter)


@register.filter(name='gettopicarray')
def gettopicarray(question):
    def safe_get_topic(qid):
        try:
            item = QuestionTopic.objects.filter(question=qid)
            return item
        except:
            return False
    retstr = []

    if safe_get_topic(question):
        for qt in safe_get_topic(question):
            str(qt.topic.id)
            retstr.append('{"value": "'+str(qt.topic.id)+'", "name": "'+str(qt.topic.topic_text)+'"}')
        return str("["+",".join(retstr)+"]")
    else:
        return str("")


@register.filter(name='istopicfollowed')
def istopicfollowed(topic, user):
    counter = FollowTopic.objects.filter(topic=topic, f_user=user).count()
    return str(counter)


@register.filter(name='gettopicfollowcount')
def gettopicfollowcount(topic):
    counter = FollowTopic.objects.filter(topic=topic).count()
    return str(counter)


@register.filter(name='istopicbooked')
def istopicbooked(topic, user):
    counter = BookTopic.objects.filter(topic=topic, b_user=user).count()
    return str(counter)


@register.filter(name='gettopicbookcount')
def gettopicbookcount(topic):
    counter = BookTopic.objects.filter(topic=topic).count()
    return str(counter)


@register.filter(name='gettopicview')
def gettopicview(topic):
    return str("topic_"+topic)


@register.filter(name='isquestionfollowed')
def isquestionfollowed(question, user):
    counter = FollowQuestion.objects.filter(question=question, f_user=user).count()
    return str(counter)


@register.filter(name='getquestionfollowcount')
def getquestionfollowcount(question):
    counter = FollowQuestion.objects.filter(question=question).count()
    return str(counter)

