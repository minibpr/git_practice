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

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('post_detail', post_id=post.id)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    images = post.image_set.all()
    comment_form = CommentForm()
    return render(request, 'post/detail.html', {
        'post': post,
        'images': images,
        'comment_form': comment_form,
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)

    return redirect('post_detail', post_id=post.id)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        delete_ids = request.POST.getlist('delete_images')
        for img_id in delete_ids:
            image = get_object_or_404(Image, id=img_id, post=post)
            image.image.delete()
            image.delete()

        for file in request.FILES.getlist('new_images'):
            Image.objects.create(post=post, image=file)

        return redirect('post_detail', post_id=post.id)

    return render(request, 'edit_post.html', {'post': post})
