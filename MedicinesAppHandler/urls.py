from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/medicine_names/', views.medicines_names_list, name='medicines_names_list'),
    path('medicines/delete_medicine_names/<int:medicine_id>/', views.medicine_name_delete, name='medicine_name_delete'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('medicines/import', views.import_medicines_names_from_csv, name='import_medicines_names_from_csv'),
    path('medicines/export/', views.export_medicines_csv, name='export_medicines_csv'),
    path('medicines/<int:medicine_id>/side_effects/', views.side_effects_list, name='side_effects_list'),
    path('medicines/<int:medicine_id>/substances/', views.substances_list, name='substances_list'),
    path('medicines/<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/<int:medicine_id>/add_side_effect/', views.add_side_effect, name='add_side_effect'),
    path('medicines/<int:medicine_id>/add_substance/', views.add_substance, name='add_substance'),
    path('medicines/delete_side_effect/<int:side_effect_id>/', views.delete_side_effect, name='delete_side_effect'),
    path('medicines/delete_substance/<int:substance_id>/', views.delete_substance, name='delete_substance'),
    path('medicines/side_effects_chart/', views.side_effects_chart, name='side_effects_chart'),
    path('medicines/download_side_effects_pdf/', views.download_side_effects_pdf, name='download_side_effects_pdf'),
    path('start/', views.start_view, name='start'),
    path('home/', views.home_view, name='home'),
]