from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import post
from django.views.generic import ListView , DetailView
from .form import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def get_date(post):
    return post['date']

class StartingPage(ListView):
    template_name = 'blog/index.html'
    model = post
    ordering = ['-date']
    context_object_name = 'posts'
    def get_queryset(self):
        query_set =  super().get_queryset()
        data = query_set[:3]
        return data

class AllPost(ListView):
    template_name = 'blog/all-post.html'
    model = post
    context_object_name = 'all_posts'

class PostDetail(View):
    def get(self, request, slug):
        posts = post.objects.get(slug = slug)
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            show = posts.id in stored_posts
        else:
            show = False    
        return render(request, 'blog/post-detail.html', {
            'comments_forms' : CommentForm(), 'post' : posts,
            'comments' : posts.comments.all().order_by('-id'),'show':show
        })  
    def post(self,request, slug):
       comment_form = CommentForm(request.POST)
       posts = post.objects.get(slug = slug)
       if comment_form.is_valid():
           comment = comment_form.save(commit = False)
           comment.post = posts
           comment.save()
           return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))  

       stored_posts = request.session.get('stored_posts')
       if stored_posts is not None:
            show = posts.id in stored_posts

       else:
            show = False 
       return render(request, 'blog/post-detail.html', {
           'comments_forms' : CommentForm() , 'post' : posts, 'comments' : posts.comments.all().order_by('-id')
           ,'show' :show       })

class Readlater(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['post'] = []
            context['has_post'] = False
        else:
            posts = post.objects.filter(id__in = stored_posts)
            context['post'] = posts
            context['has_post'] = True
        return render(request, 'blog/read_later.html', context)        
    def post(self, request):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST['post_id'])


        if post_id not in stored_posts:
              stored_posts.append(post_id)
           
        else:
              
            stored_posts.remove(post_id)  
        request.session['stored_posts'] = stored_posts     
        return HttpResponseRedirect('/')        
