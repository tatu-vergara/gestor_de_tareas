from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.lista_tareas, name='lista'),
    path('tarea/<int:indice>/', views.detalle_tarea, name='detalle'),
    path('agregar/', views.agregar_tarea, name='agregar'),
    path('eliminar/<int:indice>/', views.eliminar_tarea, name='eliminar'),
    path('registro/', views.registro, name='registro'),  
    path('editar/<int:indice>/', views.editar_tarea, name='editar'),
]
