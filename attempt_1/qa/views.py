from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Answer, VoteAnswerMod, AnswerComment, BookmarkAnswer, TopicStore, QuestionTopic, FollowTopic, BookTopic, FollowQuestion, UserProfile
from .forms import PostAnswerForm
from django.utils import timezone
from django.views import View
from django.db.models.query import QuerySet
from pprint import PrettyPrinter
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import json
from html import unescape

# Create your views here.


def dprint(object, stream=None, indent=1, width=80, depth=None):

    # Catch any singleton Django model object that might get passed in
    if getattr(object, '__metaclass__', None):
        if object.__metaclass__.__name__ == 'ModelBase':
            # Convert it to a dictionary
            object = object.__dict__

    # Catch any Django QuerySets that might get passed in
    elif isinstance(object, QuerySet):
        # Convert it to a list of dictionaries
        object = [i.__dict__ for i in object]

    # Pass everything through pprint in the typical way
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)


def home(request):
    latest_question = Question.objects.order_by('-q_pub_date')[:15]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_questions': latest_question
#    }
#    output = ", ".join(q.question_text for q in latest_question)
#    return HttpResponse(template.render(context))
    return render(request, 'qa/home.html', {'post_list': latest_question, 'active_page': 'home_new'})


def home_top(request):
    latest_question = Question.objects.order_by('-q_pub_date')[:15]
    return render(request, 'qa/home.html', {'post_list': latest_question, 'active_page': 'home_top'})


def home_bookmarked(request):
    if request.user.is_authenticated:
        aid = BookmarkAnswer.objects.filter(b_user=request.user).values_list('answer', flat=True)
        post_list = Answer.objects.filter(pk__in=aid)
        return render(request, 'qa/home.html', {'post_list': post_list, 'active_page': 'home_book'})
    else:
        return render(request, 'qa/home.html', {'post_list': None, 'active_page': 'home'})


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'qa/question_detail.html', {'question': question})


def post_answer(request, question_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostAnswerForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.answer_author = request.user
                post.question = Question.objects.get(pk=question_id)
                post.a_pub_date = timezone.now()
                post.save()
                return redirect(reverse('qa:question_detail', args=(question_id,)))
        else:
            form = PostAnswerForm()
    else:
        return redirect(reverse('qa:question_detail', args=(question_id,)))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'qa/post_answer.html', {'question': question, 'form': form})


def show_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer.objects.get(pk=answer_id)
    if answer.question.pk == question.pk:
        return render(request, 'qa/show_answer.html', {'question': question, 'answer': answer})
    else:
        return render(request, 'qa/show_answer.html', {'question': question, 'answer': answer, 'error': 'Answer does not exist for the question!'})


def edit_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer.objects.get(pk=answer_id)
    if answer.question.pk == question.pk:
        if request.user.is_authenticated:
            if request.method == "POST":
                if request.user.pk == Answer.objects.get(pk=answer_id).answer_author.pk:
                    form = PostAnswerForm(request.POST or None, instance=answer)
                    if form.is_valid():
                        post = form.save(commit=False)
                        post.a_modified_date = timezone.now()
                        post.save()
                        return redirect(reverse('qa:question_detail', args=(question_id,)))
                    else:
                        return render(request, 'qa/post_answer.html', {'question': question, 'answer': answer, 'error': 'Invalid data!'})
                else:
                    return render(request, 'qa/post_answer.html', {'question': question, 'answer': answer, 'error': 'You are not authorized to edit this answer!'})
            else:
                form = PostAnswerForm({'question': question, 'answer': answer})
        else:
            return redirect(reverse('qa:question_detail', args=(question_id,)))
    else:
        return render(request, 'qa/post_answer.html', {'question': question, 'answer': answer, 'origin': 'edit_answer', 'error': 'Answer does not exist for the question!'})
    return render(request, 'qa/post_answer.html', {'question': question, 'answer': answer, 'origin': 'edit_answer', 'form': form})


# def upvote_answer(request, question_id, answer_id):
#     question = get_object_or_404(Question, pk=question_id)
#     answer = Answer.objects.get(pk=answer_id)
#     action = request.action
#     if answer.question.pk == question.pk:
#         if request.user.is_authenticated:
#
#         else:
#             return HttpResponse("")
#     else:
#         return HttpResponse("")


class VoteAnswer(View):

    def get_upvote_count(self, answer):
        return VoteAnswerMod.objects.filter(answer=answer, action_taken=1).count()

    def get_downvote_count(self, answer):
        return VoteAnswerMod.objects.filter(answer=answer, action_taken=0).count()

    def safe_get(self, answer, vote_user):
        try:
            item = VoteAnswerMod.objects.get(answer=answer, vote_user=vote_user)
            return item
        except:
            return False

    def get(self, request, *args, **kwargs):
        aid = kwargs.get('answer_id')
        action_req = kwargs.get('action_req')
        answer = Answer.objects.get(pk=aid)
        action_item = self.safe_get(answer, request.user)

        print("action: "+action_req)
        print("aid: " + aid)
        print("enter 10")
        if answer:
            print("enter 1")
            if request.user.is_authenticated:
                print("enter 2")
                if action_item:
                    if action_item.action_taken == 1:
                        if action_req == '1':
                            action_item.delete()
                            return HttpResponse('{"success": "true","action":"unvoted","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
                        elif action_req == '0':
                            action_item.action_taken = action_req
                            action_item.save()
                            return HttpResponse('{"success": "true","action":"downvoted","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
                    elif action_item.action_taken == 0:
                        if action_req == '1':
                            action_item.action_taken = action_req
                            action_item.save()
                            return HttpResponse('{"success": "true","action":"upvoted","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
                        elif action_req == '0':
                            action_item.delete()
                            return HttpResponse('{"success": "true","action":"unvoted","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
                else:
                    if action_req == '1':
                        print("action 1")
                        action = VoteAnswerMod(answer=answer, action_taken=1, vote_user=request.user, vote_date=timezone.now())
                        action.save()
                        return HttpResponse('{"success": "true","action":"upvoted","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
                    elif action_req == '0':
                        print("action 0")
                        action = VoteAnswerMod(answer=answer, action_taken=0, vote_user=request.user, vote_date=timezone.now())
                        action.save()
                        return HttpResponse('{"success": "true","action":"downvoted","uc":"' + str(
                            self.get_upvote_count(answer)) + '","dc":"' + str(
                            self.get_downvote_count(answer)) + '"}')
            else:
                return HttpResponse('{"success": "false","error":"You are not logged in!","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')
        else:
            return HttpResponse('{"success": "false","error":"Bad request! Please reload the page and try again!","uc":"' + str(self.get_upvote_count(answer)) + '","dc":"' + str(self.get_downvote_count(answer)) + '"}')


class AddQuestion(View):

    def post(self, request):
        data = request.POST
        qtxt = data.get('question_text')
        if qtxt:
            if request.user.is_authenticated:
                question = Question(question_text=qtxt, question_author=request.user, q_pub_date=timezone.now())
                question.save()
                qid = question.id
                outstr = '{"success": "true","qid":'+str(qid)+'}'
                return HttpResponse(outstr)
            else:
                return HttpResponse('{"success": "false","error":"You are not logged in!"}')
        else:
            return HttpResponse('{"success": "false","error":"Invalid question text!"}')


class EditQuestion(View):

    def post(self, request):
        data = request.POST
        qid = data.get('question_id')
        print("Question id: "+qid)
        qtxt = data.get('question_text')
        q = Question.objects.get(pk=qid)
        if q and qtxt:
            if request.user.is_authenticated and request.user == q.question_author:
                q.question_text = qtxt
                q.q_modified_date = timezone.now()
                q.save()
                return HttpResponse('{"success": "true"}')
            else:
                return HttpResponse('{"success": "false","error":"You are not logged in or you do not have permission to make this change!"}')
        else:
            return HttpResponse('{"success": "false","error":"Question does not exist or Invalid question text!"}')


class AddAnswerComment(View):

    def safe_get(self, aid):
        try:
            item = Answer.objects.get(pk=aid)
            return item
        except:
            return False

    def post(self, request, *args, **kwargs):
        data = request.POST
        aid = data.get('aid')
        ctext = data.get('ctext')
        a = self.safe_get(aid)
        print("Answer id: " + aid)

        if a and ctext:
            if request.user.is_authenticated:
                comment = AnswerComment(answer=a, comment_text=ctext, comment_user=request.user, comment_date=timezone.now())
                comment.save()
                df = DateFormat(comment.comment_date)
                dt = df.format(get_format('DATE_FORMAT'))
                return HttpResponse('{"success": "true","cid": "'+str(comment.id)+'", "cdate": "'+str(dt)+', Just Now"}')
            else:
                return HttpResponse('{"success": "false","error":"You are not logged! Please login to comment."}')
        else:
            return HttpResponse('{"success": "false","error":"Answer does not exist or Invalid comment text!"}')


class BookAnswer(View):

    def safe_get_answer(self, aid):
        try:
            item = Answer.objects.get(pk=aid)
            return item
        except:
            return False

    def safe_get_book(self, answer, user):
        try:
            item = BookmarkAnswer.objects.filter(answer=answer, b_user=user)
            return item
        except:
            return False

    def get(self, request, *args, **kwargs):
        aid = kwargs.get('answer_id')
        action_req = kwargs.get('action_req')
        print("aid: "+aid)

        answer = self.safe_get_answer(aid)
        bookitem = self.safe_get_book(answer, request.user)

        if request.user.is_authenticated:
            if answer and not bookitem and action_req == '1':
                ba = BookmarkAnswer(answer=answer, b_user=request.user, b_date=timezone.now())
                ba.save()
                return HttpResponse('{"success": "true", "action_taken":"bookmarked"}')
            elif answer and bookitem and action_req == '0':
                ba = BookmarkAnswer.objects.get(answer=answer, b_user=request.user)
                ba.delete()
                return HttpResponse('{"success": "true", "action_taken":"unbookmark"}')
            else:
                return HttpResponse('{"success": "false","error":"Answer does not exist or illegal operation!"}')
        else:
            return HttpResponse('{"success": "false","error":"You are not loggedin! Please login and try again."}')


class SearchTopic(View):
    def safe_get_topics(self, term):
        try:
            items = TopicStore.objects.filter(topic_text__contains=term)
            return items
        except:
            return False

    def get(self, request, *args, **kwargs):
        st = kwargs.get('search_term')
        items = self.safe_get_topics(unescape(st))
        records = []
        if items:
            for i in items:
                record = {"id": str(i.id), "value": str(i.id), "name": str(i.topic_text)}
                records.append(record)
            ret = json.dumps(records)
            return HttpResponse(ret)
        else:
            return HttpResponse("{}")


class EditQuestionTopic(View):
    def safe_get_question(self, qid):
        try:
            q = Question.objects.get(pk=qid)
            return q
        except:
            return False

    def safe_get_qtopics(self, q):
        try:
            items = QuestionTopic.objects.filter(question=q)
            return items
        except:
            return False

    def safe_get_qtopic(self, q, t):
        try:
            qt = QuestionTopic.objects.get(question=q, topic=t)
            return qt
        except:
            return False

    def safe_get_topic(self, tid):
        try:
            t = TopicStore.objects.get(pk=tid)
            return t
        except:
            return False

    def post(self, request, *args, **kwargs):
        data = request.POST
        qid = kwargs.get('question_id')
        topic_list = []
        try:
            topic_str = [x.strip() for x in data.get('topic_s').strip(',').split(',')]
            topic_list = list(map(int, topic_str))
        except:
            topic_list = False

        cnt = 0
        ncnt = 0
        retvalstr = ""
        reshowstr = []
        success = {}

        question = self.safe_get_question(qid)
        question_topics = self.safe_get_qtopics(question)
        qtid = [x.topic.id for x in question_topics]

        if topic_list and question:
            if request.user.is_authenticated and request.user == question.question_author:
                print(topic_list)
                print(qtid)
                for tli in topic_list:
                    t = self.safe_get_topic(tli)
                    if t:
                        print("came here 1")
                        if tli not in qtid:
                            print("came here 1-2")
                            qt = QuestionTopic(question=question, topic=t)
                            qt.save()
                        cnt += 1
                    else:
                        ncnt += 1

                for item in qtid:
                    if item not in topic_list:
                        t = self.safe_get_topic(item)
                        qt = self.safe_get_qtopic(question, t)
                        if t and qt:
                            qt.delete()

                if len(topic_list) == cnt:
                    success["success"] = True
                    success["part"] = False
                    success["nf"] = 0
                else:
                    success["success"] = True
                    success["part"] = True
                    success["nf"] = ncnt

                for x in self.safe_get_qtopics(question):
                    retvalstr += str(x.topic.id)+","
                    retshow = {"value": str(x.topic.id), "name": str(x.topic.topic_text)}
                    reshowstr.append(retshow)
                success["retval"] = retvalstr
                success["retshow"] = reshowstr
                return HttpResponse(json.dumps(success))
            else:
                success["success"] = False
                success["error"] = "You are not logged-in or you are not permitted to perform this action."
                return HttpResponse(json.dumps(success))
        else:
            success["success"] = False
            success["error"] = "There was some error with the request or question does not exist."
            return HttpResponse(json.dumps(success))


def show_topic(request, topic_id):
    print('came here')
    qtopic = get_object_or_404(TopicStore, pk=topic_id)
    tqs = QuestionTopic.objects.filter(topic=qtopic).values_list('question', flat=True)
    questions = Question.objects.filter(pk__in=tqs)
    toptx = 'topic_'+topic_id
    return render(request, 'qa/topic.html', {'topic': qtopic, 'post_list': questions, 'active_page': toptx})


class FBTopicRel(View):

    def safe_get_topic(self, tid):
        try:
            t = TopicStore.objects.get(pk=tid)
            return t
        except:
            return False

    def safe_get_ftopic(self, t, u):
        try:
            t = FollowTopic.objects.get(topic=t, f_user=u)
            return t
        except:
            return False

    def safe_get_btopic(self, t, u):
        try:
            t = BookTopic.objects.get(topic=t, b_user=u)
            return t
        except:
            return False

    def post(self, request, *args, **kwargs):
        data = request.POST
        master = data.get('master')
        stid = kwargs.get('topic_id')
        action_req = kwargs.get('action_req')
        print("tid: " + stid)

        topic = self.safe_get_topic(stid)
        item = ""
        retstr = {}
        counter = 0

        if master == "fl":
            item = self.safe_get_ftopic(topic, request.user)
        elif master == "bk":
            item = self.safe_get_btopic(topic, request.user)

        if request.user.is_authenticated:
            if topic and not item and action_req == '1':
                if master == "fl":
                    fbt = FollowTopic(f_user=request.user, topic=topic, f_date=timezone.now())
                    fbt.save()
                    counter = FollowTopic.objects.filter(topic=topic).count()
                elif master == "bk":
                    fbt = BookTopic(b_user=request.user, topic=topic, b_date=timezone.now())
                    fbt.save()
                    counter = BookTopic.objects.filter(topic=topic).count()
                retstr["success"] = True
                retstr["action_taken"] = 1
                retstr["mast"] = master
                retstr["count"] = counter
                return HttpResponse(json.dumps(retstr))
            elif topic and item and action_req == '0':
                if master == "fl":
                    fbt = FollowTopic.objects.get(topic=topic, f_user=request.user)
                    fbt.delete()
                    counter = FollowTopic.objects.filter(topic=topic).count()
                elif master == "bk":
                    fbt = BookTopic.objects.get(topic=topic, b_user=request.user)
                    fbt.delete()
                    counter = BookTopic.objects.filter(topic=topic).count()
                retstr["success"] = True
                retstr["action_taken"] = 0
                retstr["mast"] = master
                retstr["count"] = counter
                return HttpResponse(json.dumps(retstr))
            else:
                retstr["success"] = False
                retstr["error"] = "Topic does not exist or illegal operation!"
                retstr["mast"] = master
                return HttpResponse(json.dumps(retstr))
        else:
            retstr["success"] = False
            retstr["error"] = "You are not loggedin! Please login and try again."
            retstr["mast"] = master
            return HttpResponse(json.dumps(retstr))


class FollowQuestionRel(View):

    def get_fcount(self, q, u):
        counter = FollowQuestion.objects.filter(question=q, f_user=u).count()
        return str(counter)

    def safe_get_question(self, qid):
        try:
            q = Question.objects.get(pk=qid)
            return q
        except:
            return False

    def safe_get_fq(self, q, u):
        try:
            fq = FollowQuestion.objects.get(question=q, f_user=u)
            return fq
        except:
            return False

    def post(self, request, *args, **kwargs):
        # data = request.POST
        # master = data.get('master')
        qid = kwargs.get('question_id')
        action_req = kwargs.get('action_req')
        q = self.safe_get_question(qid)
        fqr = self.safe_get_fq(q, request.user)
        retstr = {}

        if request.user.is_authenticated:
            if q and not fqr and action_req == '1':
                fq = FollowQuestion(question=q, f_user=request.user, f_date=timezone.now())
                fq.save()
                retstr["success"] = True
                retstr["action_taken"] = 1
                retstr["count"] = self.get_fcount(q, request.user)
                return HttpResponse(json.dumps(retstr))
            elif q and fqr and action_req == '0':
                fqr.delete()
                retstr["success"] = True
                retstr["action_taken"] = 0
                retstr["count"] = self.get_fcount(q, request.user)
                return HttpResponse(json.dumps(retstr))
            else:
                retstr["success"] = False
                retstr["error"] = "Question does not exist or illegal operation!"
                retstr["count"] = self.get_fcount(q, request.user)
                return HttpResponse(json.dumps(retstr))
        else:
            retstr["success"] = False
            retstr["error"] = "You are not loggedin! Please login and try again."
            retstr["count"] = self.get_fcount(q, request.user)
            return HttpResponse(json.dumps(retstr))


def user_profile(request, user_id, tab_view=''):
    def safe_get_puser(u):
        try:
            pu = UserProfile.objects.get(user=u)
            return pu
        except:
            return False
    if tab_view in ['questions', 'answers', 'following', 'followers', '']:
        if tab_view == '':
            tab_view = 'answers'

        post_list=''
        if tab_view == 'questions':
            post_list = Question.objects.filter(question_author=user_id).order_by('-q_pub_date')
        elif tab_view == 'answers':
            post_list = Answer.objects.filter(answer_author=user_id).order_by('-a_pub_date')
        puser = safe_get_puser(user_id)
        return render(request, 'qa/profile.html', {'puser': puser, 'post_list': post_list, 'active_page': tab_view})


# TODO notification
# TODO Search
# TODO user profiles
