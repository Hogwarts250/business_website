from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Post
from .forms import TopicForm, PostForm
from business.models import Club
from users.models import User

# Create your views here.
def index(request):
    """The index page for the blog."""
    topics = Topic.objects.order_by("text")
    posts = Post.objects.order_by("date_added").reverse()
    clubs = Club.objects.order_by("name")
    context = {"topics": topics, "posts": posts, "clubs": clubs}

    return render(request, "blog/index.html", context)

def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topics = Topic.objects.order_by("text")
    topic = Topic.objects.get(id=topic_id)
    posts = topic.post_set.order_by("date_added").reverse()
    clubs = Club.objects.order_by("name")
    context = {"topics": topics, "topic": topic, "posts": posts, "clubs": clubs}

    return render(request, "blog/topic.html", context)

@login_required
def user_posts(request, user_id):
    topics = Topic.objects.order_by("text")
    clubs = Club.objects.order_by("name")
    posts = User.objects.get(id=user_id).post_set.order_by("date_added").reverse
    context = {"topics": topics, "clubs": clubs, "posts": posts}

    return render(request, "blog/user.html", context)
    

@login_required
def new_post(request, topic_id=None):
    """Add a new post for a particular topic."""
    topics = Topic.objects.order_by("text")
    clubs = Club.objects.order_by("name")

    if topic_id:
        topic = Topic.objects.get(id=topic_id)
    else:
        topic = None

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = PostForm(initial={"topic": topic})
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()

            if topic_id:
                return HttpResponseRedirect(reverse("blog:topic", args=[topic_id]))
            else:
                return HttpResponseRedirect(reverse("blog:index"))

    context = {"topics": topics, "topic": topic, "form": form, "clubs": clubs}

    return render(request, "blog/new_post.html", context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    topics = Topic.objects.order_by("text")
    post = Post.objects.get(id=post_id)
    clubs = Club.objects.order_by("name")

    if request.method != "POST":
        # Initial request; pre-fill form with the current post.
        form = PostForm(instance=post)
    else:
        # POST data is submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("blog:index"))

    context = {"topics": topics, "post": post, "form": form, "clubs": clubs}

    return render(request, "blog/edit_post.html", context)
