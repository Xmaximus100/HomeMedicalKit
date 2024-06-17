from django.urls import path
from . import views

# URLConf
urlpatterns = [
    #path("", views.home),
    path('todos/', views.todos, name="Todos"),
    path('index/', views.index),
    path("import/", views.importExcel, name="push_excel"),
    path('hello/', views.say_hello),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('medicines/export/', views.export_medicines_csv, name='export_medicines_csv'),
    path('medicines/side_effects_chart/', views.side_effects_chart, name='side_effects_chart'),
    path('', views.start_view, name='start'),
    path('', views.home_view, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup')
]