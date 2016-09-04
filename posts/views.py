from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from .models import Post
from .forms import PostForm



def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "Successfully Created!")
        return HttpResponseRedirect(post.get_absolute_url())
    # else:
    #     messages.error(request, "Not Successfully Created!")
    return render(request, 'post_form.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    return render(request, 'post_detail.html', {'post': post})


def post_list(request):
    today = timezone.now().date()
    all_posts = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        all_posts = Post.objects.all()
    query = request.GET.get("q")
    if query:
        all_posts = all_posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()
    paginator = Paginator(all_posts, 1)
    page_var = "p"
    page = request.GET.get(page_var)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts': posts, 'page_var': page_var, 'today': today})


def post_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully Edited!")
        return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'post_form.html', {'post': post, 'form': form})


def post_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect("posts:list")