from django.urls import path

from .views import index, add_input, delete_input, add_user

app_name = "polls_app"
urlpatterns = [
    path("", index, name="index"),
    path("add/", add_input, name="add"),
    path("delete/", delete_input, name="delete"),
    path("add_user/", add_user, name="add_user"),
]