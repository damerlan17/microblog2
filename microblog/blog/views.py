from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Profile, Like, Comment
from django.core.paginator import Paginator

# Главная страница — последние 50 постов
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10  # пагинация

    def get_queryset(self):
        return Post.objects.all().order_by('-created_on')[:50]

# Регистрация
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

# Профиль
class ProfileView(DetailView):
    model = Profile
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'bio']
    template_name = 'blog/profile_edit.html'
    success_url = '/'

    def get_object(self):
        return self.request.user.profile

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('home')
    template_name = 'blog/profile_confirm_delete.html'

    def get_object(self):
        return self.request.user.profile

# Посты
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Лайки
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', pk=pk)

# Комментарии
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('post_detail', pk=pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


def home(request):
    posts = Post.objects.all().order_by('-created_at')[:50]

    # Добавляем флаг "уже лайкнул?"
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.like_set.filter(user=request.user).exists()
    else:
        for post in posts:
            post.user_has_liked = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'page_obj': page_obj})