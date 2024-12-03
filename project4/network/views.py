from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from .forms import PostForm
from .models import User, Posts, Likes, Follow
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data.get('content')
                new_post = Posts(content=content, user=request.user)
                new_post.save()
                context = {
                    'form': PostForm(),
                    'posts': Posts.objects.all(),
                    'likes': Likes.objects.filter(user=request.user)
                }
                return redirect(reverse('index'))
    else:
        context = {

            'posts': Posts.objects.all().order_by('-id'),

        }
        return render(request, "network/index.html", context)

    likes = Likes.objects.all()
    t = []
    counter = []
    for like in likes:
        counter.append(like.post_id)
        if like.user_id == request.user.id:
            t.append(like.post_id)

    context = {
        'form': PostForm(),
        'posts': Posts.objects.all().order_by('-id'),
        'likes': Likes.objects.filter(user=request.user),
        't': t,
        "counter": counter
    }
    return render(request, "network/index.html", context)


def like(request, post_id):
    if request.method == "POST":
        # data = json.loads(request.body)
        # print(data)
        post = Posts.objects.filter(pk=post_id).first()
        like = Likes.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            post.like -= 1
            post.save()
        else:
            new_like = Likes(post=post, user=request.user)
            post.like += 1
            new_like.save()
            post.save()

        return JsonResponse({'status': 'success'})


        # return redirect(reverse('index'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'network/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.request.user.id
        context['following_count'] = Follow.objects.filter(user=user_id).count()
        context['follower_count'] = Follow.objects.filter(user_follower=user_id).count()
        context['posts'] = Posts.objects.filter(user=user_id).order_by('-id')
        context['users'] = User.objects.filter(~Q(id=user_id))
        follow = Follow.objects.filter(user_id=user_id)
        f = []
        for i in follow:
            f.append(i.user_follower_id)
        context['fs'] = f
        return context


@csrf_exempt
def add_follower(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        # پردازش داده‌ها
        print(data)
        if data['key1'] == 'unfollow':
            if Follow.objects.filter(user_id=request.user.id, user_follower_id=data['key2']).exists():

                follow = Follow.objects.filter(user_id=request.user.id, user_follower_id=data['key2']).delete()

        else:

            new_follow = Follow(user_id=request.user.id, user_follower_id=data['key2'])
            new_follow.save()
    return JsonResponse({'status': 'success'})


@method_decorator(login_required, name='dispatch')
class FollowingListView(TemplateView):
    template_name = 'network/following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.request.user.id
        following = Follow.objects.filter(user_id=user_id)
        context['posts'] = Posts.objects.all().order_by('-id')
        ff = []
        for i in following:
            ff.append(i.user_follower_id)
        context['following'] = ff

        likes = Likes.objects.all()
        t = []
        counter = []
        for like in likes:
            counter.append(like.post_id)
            if like.user_id == user_id:
                t.append(like.post_id)
        context['t'] = t
        return context


class EditPostView(UpdateView):
    template_name = 'network/edit_post.html'
    model = Posts
    form_class = PostForm

    # success_url = reverse('profile' k)

    def get_success_url(self):
        print(self.get_object().id)
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    # def get_context_data(self, **kwargs):
    #     context = super(EditPostView, self).get_context_data(**kwargs)
    #     context['form'] = Posts()
    #     return context