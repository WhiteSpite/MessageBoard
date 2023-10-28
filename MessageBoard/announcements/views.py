from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.paginator import Paginator
from datetime import datetime
from .models import Announcement, Response
from .filters import AnnouncementFilter, MyAnnouncementFilter, ResponseFilter
from .forms import AnnouncementForm
from MessageBoard.settings import LOGIN_URL


class AnnouncementList(ListView):
    model = Announcement
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_res = AnnouncementFilter(
            self.request.GET, queryset=queryset)
        self.posts_num = queryset.qs.count()
        return queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter_res
        context['time_now'] = datetime.utcnow()
        context['posts_name'] = 'Все объявления'
        context['posts_num'] = self.posts_num
        context['post_name'] = 'объявление'
        context['app_name'] = 'announcements'
        if self.request.user.is_authenticated:
            context['subscribed'] = self.request.user.profile.subscribed_to_announcements
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = 'announcements'
        responses = context['post'].responses.all().order_by('-created_at')
        number_per_page = 10
        paginator = Paginator(responses, number_per_page)
        if responses.count() > number_per_page:
            context['is_paginated'] = True
        else:
            context['is_paginated'] = False
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['user_is_owner'] = self.request.user == context['post'].user
        if self.request.user.is_authenticated:
            responses_qs = context['post'].responses.filter(
                user=self.request.user)
            context['response_by_user_exist'] = responses_qs.exists()
            if context['response_by_user_exist']:
                context['response_by_user'] = responses_qs.first()
        return context
    
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)
        Response.objects.create(
            text=request.POST.get('text'),
            user=request.user,
            announcement=self.get_object()
        )
        return redirect(self.request.path)


class MyAnnouncementList(LoginRequiredMixin, ListView):
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Announcement.objects.filter(user=self.request.user)
        queryset = self.filter_res = MyAnnouncementFilter(
            self.request.GET, queryset=queryset)
        self.posts_num = queryset.qs.count()
        return queryset.qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter_res
        context['time_now'] = datetime.utcnow()
        context['posts_name'] = 'Мои объявления'
        context['posts_num'] = self.posts_num
        context['post_name'] = 'объявление'
        context['app_name'] = 'announcements'
        return context


class AnnouncementEdit(UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'post_edit.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'объявление'
        return context

    def test_func(self):
        announcement = self.get_object()
        return self.request.user == announcement.user


class AnnouncementAdd(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'post_add.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'объявление'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('announcements:post', kwargs={'pk': self.object.pk})


class AnnouncementDelete(UserPassesTestMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Announcement
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = '/announcements/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'объявление'
        return context

    def test_func(self):
        announcement = self.get_object()
        return self.request.user == announcement.user


class ResponseList(LoginRequiredMixin, ListView):
    template_name = 'responses.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Response.objects.filter(
            announcement__user=self.request.user)
        filter_args = {'current_username': self.request.user.username}
        queryset = self.filter_res = ResponseFilter(
            self.request.GET, queryset=queryset, **filter_args)
        self.posts_num = queryset.qs.count()
        return queryset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter_res
        context['time_now'] = datetime.utcnow()
        context['posts_num'] = self.posts_num
        context['posts_name'] = 'Отклики'
        return context


@login_required
def accept_response(request):
    response = Response.objects.get(id=request.GET.get('response_id'))
    if response.announcement.user == request.user and not response.is_accepted:
        response.is_accepted = True
        response.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_response(request):
    response = Response.objects.get(id=request.GET.get('response_id'))
    if response.announcement.user == request.user or response.user == request.user:
        response.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_all_responses_by_post(request):
    announcement = Announcement.objects.get(id=request.GET.get('announcement_id'))
    if announcement.user == request.user:
        responses = Response.objects.filter(announcement=announcement)
        for response in responses:
            response.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_all_responses(request):
    responses = Response.objects.filter(announcement__user=request.user)
    for response in responses:
        response.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def subscribe(request):
    profile = request.user.profile
    if not profile.subscribed_to_announcements:
        profile.subscribed_to_announcements = True
        profile.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe(request):
    profile = request.user.profile
    if profile.subscribed_to_announcements:
        profile.subscribed_to_announcements = False
        profile.save()
    return redirect(request.META.get('HTTP_REFERER'))
