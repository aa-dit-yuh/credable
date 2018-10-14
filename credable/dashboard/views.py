from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView


User = get_user_model()


class UserDashboard(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'pages/home.html'

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_dashboard = UserDashboard.as_view()