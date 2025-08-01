from django.urls import path
from .import views

urlpatterns = [
    path('', views.PostListCreateAPIView.as_view()), # GET -> list, POST-> create
    path('<int:id>/', views.PostDetailAPIView.as_view()), # GET -> item, PUT ->update, DELETE -> destroy
    path('<int:id>/comments/', views.CommentListCreateAPIView.as_view()),

]