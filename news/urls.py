from django.urls import path
from news import views

urlpatterns = [
    path('', views.LatestPostsList.as_view()),
    path('all/', views.AllPostsList.as_view()),
    path('read/', views.ReadPostList.as_view()),
    # path('<slug:category_slug>/<slug:post_slug>/', views.PostDetail.as_view()),
    path('top/', views.TopViewPost.as_view()),

    path('<slug:category_slug>/', views.CategoryDetail.as_view()),


    # path('comments/', views.CommentsList.as_view()),
    # path('products/search/', views.search),
]