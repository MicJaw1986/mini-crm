from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('', views.interaction_list, name='interaction_list'),
    path('timeline/', views.interaction_timeline, name='interaction_timeline'),
    path('<int:pk>/', views.interaction_detail, name='interaction_detail'),
    path('create/', views.interaction_create, name='interaction_create'),
    path('<int:pk>/update/', views.interaction_update, name='interaction_update'),
    path('<int:pk>/delete/', views.interaction_delete, name='interaction_delete'),
]
