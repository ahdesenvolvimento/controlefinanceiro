from django.urls import path
from .views import IndexView, adicionar, retirar, despesa
urlpatterns = [
    path('', IndexView, name='index'),
    path('adicionar/', adicionar, name='adicionar'),
    path('retirar/', retirar, name='retirar'),
    path('despesas/', despesa, name='despesa'),
]