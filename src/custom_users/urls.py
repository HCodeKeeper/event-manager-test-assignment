from django.urls import path

from custom_users.views import MeView, UserView

urlpatterns = [
    path("", UserView.as_view()),
    path("<int:pk>/", UserView.as_view()),
    path("me/", MeView.as_view()),
]
