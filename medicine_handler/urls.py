from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("", views.home),
    path('todos/', views.todos, name="Todos"),
    path('index/', views.index),
    path("import/", views.importExcel, name="push_excel"),
    path('hello/', views.say_hello)
]