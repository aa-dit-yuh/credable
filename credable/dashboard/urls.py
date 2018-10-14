from django.urls import path

from .views import (
	user_dashboard,
)

app_name = "dashboard"
urlpatterns = [
    path("", view=user_dashboard, name="home"),
]
