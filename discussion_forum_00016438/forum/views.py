from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Post, Topic, Comment
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

class PostListView(ListView):
  model = Post
  template_name = 'forum/post_list.html'
  context_object_name = 'posts'

  def get_queryset(self):
    query = self.request.GET.get('q')
    if query:
      return Post.objects.filter(
          Q(title__icontains=query) | Q(body__icontains=query)
      )
    return Post.objects.all().order_by('-created_at')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['search_query'] = self.request.GET.get('q', '')
    return context

class PostDetailView(FormMixin, DetailView):
  model = Post
  template_name = 'forum/post_detail.html'
  form_class = CommentForm

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid() and request.user.is_authenticated:
      comment = form.save(commit=False)
      comment.post = self.object
      comment.author = request.user
      comment.save()
      return redirect('post_detail', slug=self.object.slug)
    return self.get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['topic', 'title', 'body', 'tags']
  template_name = 'forum/post_form.html'
  success_url = reverse_lazy('post_list')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['topic', 'title', 'body', 'tags']
  template_name = 'forum/post_form.html'

  def test_func(self):
    return self.request.user == self.get_object().author

  def get_success_url(self):
    return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'forum/post_confirm_delete.html'
  success_url = reverse_lazy('post_list')

  def test_func(self):
    return self.request.user == self.get_object().author
      
class SignUpView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'registration/signup.html'