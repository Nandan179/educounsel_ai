from django.urls import path
from .views import (
    dashboard,
    chatbot,
    filter_ui,
    view_policies,
    compare_universities,
    login_view,
    signup_view,
    logout_view,
)

urlpatterns = [
    path("",                         login_view,           name="login"),
    path("signup/",                  signup_view,          name="signup"),
    path("logout/",                  logout_view,          name="logout"),
    path("dashboard/",               dashboard,            name="dashboard"),
    path("chatbot/",                 chatbot,              name="chatbot"),
    path("filter/",                  filter_ui,            name="filter"),
    path("policies/<int:university_id>/", view_policies,   name="policies"),
    path("compare/",                 compare_universities, name="compare"),
]
