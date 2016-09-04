from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm



def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully Created!")
        return HttpResponseRedirect(post.get_absolute_url())
    # else:
    #     messages.error(request, "Not Successfully Created!")
    return render(request, 'post_form.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})


def post_list(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 4)
    page_var = "p"
    page = request.GET.get(page_var)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts': posts, 'page_var': page_var})


def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully Edited!")
        return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'post_form.html', {'post': post, 'form': form})


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect("posts:list")