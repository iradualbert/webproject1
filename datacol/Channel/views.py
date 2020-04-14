import secrets
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse,HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Channel, Topic, ProductService, Subscriber, Question
from .forms import CreateChannel, CreateChannelTopic, CreateQuestion, CreateAnswer
from .lazy_loading import lazy_loading_forms

class ProductDetailView(DetailView):
    model = ProductService

class ChannelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Channel
    fields = ['channel_name', 'channel_username', 'channel_profile_pic', 'bio', 'website',
              'private', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        channel = self.get_object()
        if self.request.user == channel.owner:
            return True
        return False

class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateQuestion
    template_name = 'channel/create_question.html'
    redirect_field_name = 'home_page'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return lazy_loading_forms(request, self.form_class, form_type='question_form_ajax')
        channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        form = self.form_class()
        form.fields["question_topic"].queryset = Topic.objects.filter(parent_channel=channel_info)
        if channel_info:
            return render(request, self.template_name, {'form':form, 'title': 'Add Question'})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user_info = user
        channel = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        self.object.channel_info = channel
        from User.models import Notification
        Notification.send_notification(to=channel.owner, url=self.get_success_url(),
                                       to_channel=True, notification_type='new_question',
                                       description=f"<small>New question '<b>{self.object.question_title}</b>'has been asked to your channel</small>")
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Question Saved Successfully!")
        return reverse('home_page')

class AnswerCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateAnswer
    template_name = 'channel/answer_form.html'
    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])

        if channel_info.private:
            if channel_info.is_admin(current_user) or channel_info.owner == current_user:
                question_info = get_object_or_404(Question, pk=self.kwargs['pk'])
                form = self.form_class()
                if channel_info:
                    return render(request, self.template_name,
                                  {'form': form, 'title': 'Add Answer', 'question': question_info})
            else:
                return HttpResponseForbidden()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_info = self.request.user
        self.object.channel_info = get_object_or_404(Channel, channel_code=self.kwargs['channel_code'])
        self.object.question_info= get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Question Saved Successfully!")
        return reverse('home_page')



@login_required
def create_channel(request):
    try:
        channel = Channel.objects.get(owner=request.user)
        channel_code = channel.channel_code
        return redirect('channel-detail', channel_code=channel_code)
    except:
        if request.method == 'POST':
            form = CreateChannel(request.POST)
            if form.is_valid():
                channel_code = secrets.token_hex(8)
                ## Make sure the channel with the same channel_code does not exist
                channel = Channel.objects.filter(channel_code=channel_code)
                if channel:
                    while True:
                        channel_code = secrets.token_hex(8)
                        channel = Channel.objects.filter(channel_code=channel_code)
                        if channel:
                            pass
                        else:
                            break
                user = request.user
                channel_name = form.cleaned_data['channel_name']
                channel_username = form.cleaned_data['channel_username']
                website = form.cleaned_data['website']
                bio = form.cleaned_data['description']
                new_channel = Channel(owner=user,
                                      channel_name=channel_name,
                                      channel_code=channel_code,
                                      channel_username=channel_username,
                                      website=website,
                                      bio=bio,)
                new_channel.save()
                messages.success(request, f'Channel Created Successfully!')
                return redirect('channel-detail', channel_code=channel_code)
        else:
           form = CreateChannel()
        return render(request, 'channel/channel_form.html', {'form': form, 'title': 'Create A Channel'})

@login_required
def create_channel_topic(request, channel_code):
    current_user = request.user
    channel = get_object_or_404(Channel, channel_code=channel_code)
    if channel.owner == current_user:
        if request.method == 'POST':
            form = CreateChannelTopic(request.POST)
            if form.is_valid():
                topic_title = form.cleaned_data['title_name']
                website = form.cleaned_data['link']
                description = form.cleaned_data['description']
                new_topic = Topic(topic_title=topic_title,
                                  website=website,
                                  parent_channel=channel,
                              )
                if description:
                    new_topic.description = description
                new_topic.save()
                if request.is_ajax():
                    return JsonResponse({"status": "ok"})
                else:
                    messages.success(request, 'Created')
                    return redirect('channel-detail', channel_code=channel_code)
        else:
            form = CreateChannelTopic()
    else:
        return HttpResponseForbidden()
    return render(request, 'channel/topic_form.html', {'form':form, 'title': f'{channel.channel_name} - New'})


def channel_home(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    questions = Question.objects.filter(channel_info=channel)
    user = request.user
    if user.is_authenticated:
        sub_status = channel.is_subscribed(user)
        if sub_status:
            sub_button = 'Subscribed'
        else:
            sub_button = 'Subscribe'
    else:
        sub_button = 'Subscribe'
    t_form = CreateChannelTopic()
    return render(request, 'channel/channel_detail.html', {'title': channel.channel_username, 'object': channel, 't_form': t_form, 'sub_button_text': sub_button, 'questions': questions})
@require_POST
def channel_subscribe(request, channel_code):
    user = request.user
    if request.is_ajax() and user.is_authenticated:
        try:
            channel = Channel.objects.get(channel_code=channel_code)
        except ObjectDoesNotExist:
            return JsonResponse({"response": "channel not found", "status": "ok"})
        if channel.owner == user:
            return JsonResponse({"response": "invalid request", "status": "ok"})
        subscriber = Subscriber.objects.filter(channel_id=channel.id, user_id=user.id)
        if subscriber:
            channel.remove_subscriber(user=user)
            return JsonResponse({"response": "Unsubscribed", "status": "ok"})
        else:
            channel.add_subscriber(user=user)
            return JsonResponse({"response": "Subscribed", "status": "ok"})
    else:
        return HttpResponseNotAllowed('405')

def channel_add_admin(request, channel_code):
    channel = get_object_or_404(Channel, channel_code=channel_code)
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        return JsonResponse({'success': False, 'status': 'not_found'})

    current_user = request.user
    if (current_user != channel.owner):
        return JsonResponse({'success': False, 'status': 'Invalid'})

    if channel.is_admin(user):
        channel.remove_admin(user)
        return JsonResponse({'success': True, 'status': 'removed'})

    else:
        channel.add_admin(user)
        return JsonResponse({'success': True, 'status': 'ok'})

