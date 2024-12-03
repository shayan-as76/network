
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("add_follower/", views.add_follower, name="add_follower"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following/", views.FollowingListView.as_view(), name="following"),
    path("edit_post/<pk>", views.EditPostView.as_view(), name="edit-post"),

]
