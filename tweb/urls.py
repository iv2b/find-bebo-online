"""tweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

import tweb
from tweb.views import HomePageView, UserCreateView, BlogListView, BlogDetailView, UserDetailView, UserChangeAvatarView, \
    LeaderboardListView, ScoreViewSet, UserInfoGetApiView, PostCreateView

score_router = SimpleRouter()
score_router.register('api/scores', ScoreViewSet, basename="scores")

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', UserCreateView.as_view(), name="signup"),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("blog/<int:pk>", BlogDetailView.as_view(), name="post"),
    path("blog/makePost/", staff_member_required(PostCreateView.as_view()), name="writePost"),
    path("user/", login_required(UserDetailView.as_view()), name="userpage"),
    path("user/changeAvatar/<int:avatar>", UserChangeAvatarView, name="changeAvatar"),
    path("leaderboard/", LeaderboardListView.as_view(), name="leaderboard"),
    path("api/get-auth-token", obtain_auth_token, name="api-get-auth-token"),
    path("api/get-user-info", UserInfoGetApiView.as_view(), name="api-get-user-info")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + score_router.urls
