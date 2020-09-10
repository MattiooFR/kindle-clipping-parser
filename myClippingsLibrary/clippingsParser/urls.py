from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:library>/', views.library, name='library'),
    path('<str:library_title>/<int:book_id>/', views.book, name='book')
]
