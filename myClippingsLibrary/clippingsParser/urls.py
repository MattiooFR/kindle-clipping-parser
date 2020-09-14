from django.urls import path

from . import views

app_name = 'clippingsParser'
urlpatterns = [
    path('', views.index, name='index'),
    path('library/<str:library>/', views.library, name='library'),
    path('book/<int:book_id>/', views.book, name='book')
]
