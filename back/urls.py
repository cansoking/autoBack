from django.urls import path
from back import views

urlpatterns = [
    path('index', views.index),
    path('login', views.login),
    path('modify_user', views.modify_user),
    path('check', views.check),
    path('get_errors', views.get_errors),
    path('deactive_question', views.deactive_question),
    path('get_logs', views.get_logs),
    path('delete_log', views.delete_log),
    path('mark_question', views.mark_question),
    path('get_random_questions', views.get_random_questions),
    path('get_advice', views.get_advice),
]
