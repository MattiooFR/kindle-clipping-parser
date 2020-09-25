from django.urls import path

from . import views

app_name = 'clippingsParser'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('library/<str:library>/', views.LibraryView.as_view(), name='library'),
    path('book/<int:pk>/', views.BookView.as_view(), name='book')
]
