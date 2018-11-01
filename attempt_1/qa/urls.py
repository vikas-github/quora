from django.conf.urls import url
from . import views
from .views import VoteAnswer, AddQuestion, EditQuestion, AddAnswerComment, BookAnswer, SearchTopic, EditQuestionTopic, FBTopicRel, FollowQuestionRel


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^(?P<question_id>[0-9]+)/$', views.question_detail, name="question_detail"),
    url(r'^(?P<question_id>[0-9]+)/answer$', views.post_answer, name="post_answer"),
    url(r'^(?P<question_id>[0-9]+)/answer/edit/(?P<answer_id>[0-9]+)$', views.edit_answer, name="edit_answer"),
    url(r'^(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/vote/(?P<action_req>[0,1])$', VoteAnswer.as_view(), name="vote_answer"),
    url(r'^(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/comment$', AddAnswerComment.as_view(), name="add_comment"),
    url(r'^(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)$', views.show_answer, name="show_answer"),
    url(r'^add_question$', AddQuestion.as_view(), name="add_question"),
    url(r'^edit_question$', EditQuestion.as_view(), name="edit_question"),
    url(r'^top_stories$', views.home_top, name="top_stories"),
    url(r'^bookanswer/(?P<answer_id>[0-9]+)/(?P<action_req>[0,1])$', BookAnswer.as_view(), name="book_answer"),
    url(r'^bookmarked_answers', views.home_bookmarked, name="bookmarked_answers"),
    url(r'^topic_search/(?P<search_term>[a-z,A-Z,0-9]+)/$', SearchTopic.as_view(), name="search_topic"),
    url(r'^edit_question_topics/(?P<question_id>[0-9]+)$', EditQuestionTopic.as_view(), name="edit_question_topic"),
    url(r'^topic/(?P<topic_id>[0-9]+)$', views.show_topic, name="show_topic"),
    url(r'^fb_topic/(?P<topic_id>[0-9]+)/(?P<action_req>[0,1]+)$', FBTopicRel.as_view(), name="fb_topic"),
    url(r'^follow_question/(?P<question_id>[0-9]+)/(?P<action_req>[0,1]+)$', FollowQuestionRel.as_view(), name="follow_question"),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.user_profile, name="user_profile"),
    url(r'^profile/(?P<user_id>[0-9]+)/(?P<tab_view>(questions|answers|followers|following))$', views.user_profile, name="user_profile"),
]


