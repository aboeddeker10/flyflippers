from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process', views.process),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('create_item', views.create),##handles form data
    path('items/new', views.new),
    path('items/edit/<int:item_id>', views.edit),
    path('<int:item_id>/delete', views.delete),
    path('<int:item_id>/update', views.update),
    path('items/<int:item_id>', views.details),
    path('<int:item_id>/favorite', views.favorite),
    path('<int:item_id>/unfavorite', views.unfavorite),
    path('gallery', views.gallery)
]

