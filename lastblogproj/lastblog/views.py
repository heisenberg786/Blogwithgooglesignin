from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from lastblog.models import Post
from lastblog.forms import UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
def base(request):
    return render(request,'lastblog/base.html')
# def home(request):
#     post = Post.objects.all()
#     return render(request,'lastblog/home.html',{'post':post})
class PostListView(ListView):
    model = Post
    template_name = 'lastblog/home.html'
    context_object_name = 'post'
    ordering = ['-date_created']

class PostDetailView(DetailView):
    model = Post
    template_name = 'lastblog/postdetail.html'

class PostCreateView(LoginRequiredMixin,CreateView):

    model = Post
    fields = ['title','content']
    template_name = 'lastblog/createpost.html'
    success_url = '/home/'
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    model = Post
    fields = ['title','content']
    template_name = 'lastblog/createpost.html'
    success_url = '/home'
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Post
    fields = ['title','content']
    template_name = 'lastblog/deletepost.html'
    success_url = '/home/'
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            username = form.cleaned_data['username']
            messages.success(request,f'{username} is registered Successfully')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserForm()
    return render(request,'lastblog/register.html',{'form':form})
