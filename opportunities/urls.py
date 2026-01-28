"""
URL routing dla aplikacji Opportunities

CZYTAJ KOMENTARZE - Routing dla CRUD + dodatkowa akcja move_stage!
"""

from django.urls import path
from . import views

# Namespace - pozwala używać {% url 'opportunities:opportunity_list' %}
app_name = 'opportunities'

urlpatterns = [
    # Lista opportunities
    # URL: /opportunities/
    path('', views.opportunity_list, name='opportunity_list'),

    # Nowa opportunity
    # URL: /opportunities/new/
    path('new/', views.opportunity_create, name='opportunity_create'),

    # Szczegóły opportunity
    # URL: /opportunities/5/
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),

    # Edycja opportunity
    # URL: /opportunities/5/edit/
    path('<int:pk>/edit/', views.opportunity_update, name='opportunity_update'),

    # Usunięcie opportunity
    # URL: /opportunities/5/delete/
    path('<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),

    # Przesunięcie do nowego stage (dodatkowa akcja!)
    # URL: /opportunities/5/move/proposal/
    path('<int:pk>/move/<str:new_stage>/', views.opportunity_move_stage, name='opportunity_move_stage'),
]

# PODSUMOWANIE - Co się nauczyłeś:
# 1. app_name - namespace dla URL
# 2. <int:pk> - parametr URL typu integer
# 3. <str:new_stage> - parametr URL typu string
# 4. name= - nazwa dla reverse() i {% url %}
# 5. Kolejność ma znaczenie! (new/ przed <int:pk>/)
