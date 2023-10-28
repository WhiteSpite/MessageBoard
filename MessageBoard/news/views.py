from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import datetime
from .models import News
from .filters import NewsFilter
from .forms import NewsForm

  
class NewsList(ListView):
    model = News
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_res = NewsFilter(
            self.request.GET, queryset=queryset)
        self.posts_num = queryset.qs.count()
        return queryset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter_res
        context['posts_name'] = 'Все новости'
        context['time_now'] = datetime.utcnow()
        context['posts_num'] = self.posts_num
        context['post_name'] = 'новость'
        context['app_name'] = 'news'
        context['user_is_manager'] = self.request.user.groups.filter(name='managers').exists()
        if self.request.user.is_authenticated:
            context['subscribed'] = self.request.user.profile.subscribed_to_news
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'post.html'
    context_object_name = 'post'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = 'news'
        context['user_is_owner'] = self.request.user == context['post'].user
        return context
    

class NewsEdit(UserPassesTestMixin, UpdateView):
    permission_required = ('news.change_post')
    model = News
    form_class = NewsForm
    template_name = 'post_edit.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'новость'
        return context
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.user and \
            self.request.user.groups.filter(name='managers').exists()


class NewsAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news')
    model = News
    form_class = NewsForm
    template_name = 'post_add.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'новость'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('news:post', kwargs={'pk': self.object.pk})


class NewsDelete(UserPassesTestMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = News
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = '/news/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_name'] = 'новость'
        return context
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.user and \
            self.request.user.groups.filter(name='managers').exists()
    
    
@login_required
def subscribe(request):
    profile = request.user.profile
    if not profile.subscribed_to_news:
        profile.subscribed_to_news = True
        profile.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe(request):
    profile = request.user.profile
    if profile.subscribed_to_news:
        profile.subscribed_to_news = False
        profile.save()
    return redirect(request.META.get('HTTP_REFERER'))
