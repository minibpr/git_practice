from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Image
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            for img in request.FILES.getlist('images'):
                Image.objects.create(post=post, image=img)
            return redirect('post_detail', pk=post.pk)
    else:
        post_form = PostForm()
    return render(request, 'post/form.html', {'post_form': post_form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post_detail', pk=pk)
    else:
        post_form = PostForm(instance=post)

    return render(request, 'post/update.html', {'post_form': post_form})

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post/list.html', {'posts': posts})
