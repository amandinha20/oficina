from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.lista_veiculos, name='lista'),
    path('novo/', views.novo_veiculo, name='novo'),
    path('editar/<int:veiculo_id>/', views.editar_veiculo, name='editar'),
    path('excluir/<int:veiculo_id>/', views.excluir_veiculo, name='excluir'),
]
