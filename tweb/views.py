from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from rest_framework import viewsets, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from tweb.forms import CustomUserCreationForm
from tweb.models import CustomUser, BlogPost, Score
from tweb.serializers import ScoreSerializer, AvatarSerializer


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['userAvatar'] = get_object_or_404(CustomUser, pk=self.request.user.id).avatar
        return context


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        valid = super(UserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class PostCreateView(CreateView):
    model = BlogPost
    template_name = "blogPost/writePost.html"
    success_url = reverse_lazy("blog")
    fields = ['title','content','image','areCommentsAllowed']

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super(PostCreateView, self).form_valid(form)


class BlogListView(ListView):
    model = BlogPost
    template_name = "blogPost/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blogPost/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UserDetailView(TemplateView):
    template_name = "user/userpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()

        rating = Score.objects.filter(user=self.request.user).order_by("-rating").first()

        if rating is not None:

            rank = Score.objects.filter(rating__gt=rating.rating).count()
            context['score'] = int(rating.rating)
            context['rank'] = rank + 1
        else:
            context['score'] = -1
            context['rank'] = -1
        return context


def UserChangeAvatarView(request, avatar):
    CustomUser.objects.filter(user=request.user).update(avatar=avatar)
    # return render(request, "user/userpage.html")
    return redirect(reverse('userpage'))


class LeaderboardListView(ListView):
    model = Score
    template_name = "leaderboard/leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        ratings = Score.objects.order_by("-rating")[:20]
        avatars = []

        for r in ratings:
            try:
                avatars.append(CustomUser.objects.filter(pk=r.user.id).first().avatar)
            except:
                avatars.append(0)

        #context['avatars'] = avatars

        if self.request.user.is_authenticated:
            nearRatings = []
            nearRanks = []
            nearAvatars = []
            rating = Score.objects.filter(user=self.request.user).order_by("-rating").first()
            if rating is not None:
                rank = Score.objects.filter(rating__gt=rating.rating).count()
                minRank = rank - 5
                maxRank = rank + 5

                maxRank = maxRank + 1

                if minRank < 0:
                    minRank = 0

                if maxRank > ratings.count():
                    maxRank = ratings.count()

                for x in range(minRank, maxRank):
                    nearRatings.append(ratings[x])
                    nearRanks.append(x + 1)

                for x in range(len(nearRatings)):
                    if nearRatings[x].user == self.request.user:
                        rank = x + 1
                        break

                for r in nearRatings:
                    try:
                        nearAvatars.append(CustomUser.objects.filter(pk=r.user.id).first().avatar)
                    except:
                        nearAvatars.append(0)

                nearScores = zip(nearRatings, nearRanks, nearAvatars)
                context['nearScores'] = nearScores
                context['nearRank'] = rank
            else:
                context['nearRank'] = -1

        ratings = list(zip(ratings, avatars))
        context['scores'] = ratings
        return context


class UserInfoGetApiView(RetrieveAPIView):
    model = CustomUser
    serializer_class = AvatarSerializer

    def get(self, request):
        user = self.request.user
        avatar = CustomUser.objects.filter(user=user).first().avatar
        rating = Score.objects.filter(user=self.request.user).order_by("-rating").first()
        if rating is not None:
            rank = Score.objects.filter(rating__gt=rating.rating).count() + 1
            rating = rating.rating
        else:
            rank = "N/A"
            rating = "N/A"
        return Response({"avatar": avatar, "id": user.id, "name": user.username, "rating": rating, "rank": rank})


class ScoreViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def create(self, request, *args, **kwargs):
        user = None
        existingRating = None
        # newRating = self.request.query_params.get('rating', 0)
        newRating = self.request.data['rating']
        newRating = float(newRating)
        checkedData = request.data
        # checkedData._mutable = True
        if self.request and hasattr(self.request, "user"):
            user = self.request.user

        if not request.POST.get('user', False):
            checkedData['user'] = user.pk

        if user.pk is not None:
            existingRating = Score.objects.filter(user=user.pk).order_by("-rating").first()

        if existingRating is not None:
            if str(user.pk) != str(self.request.data['user']):
                return Response({"Status": "WrongUser, expected: " + str(user.pk) + "but received: " + str(
                    self.request.data['user'])})

            if newRating > existingRating.rating:
                self.kwargs['pk'] = existingRating.pk
                return self.update(request, *args, **kwargs)
            else:
                return Response({"Status": "NoUpdateNeeded"})
        else:
            serializer = self.get_serializer(data=checkedData)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
