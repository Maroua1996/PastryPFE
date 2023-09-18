from django.urls import path




from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('articles/', articles, name='articles'),
    path('category/<slug:slug>/', category_articles, name='category_articles'),
    path('tag/<slug:slug>/', tag_articles, name='tag_articles'),
    path('article/<slug:slug>/', details_articles, name='details_articles'),
    path('add_reply/<int:article_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('like/<int:pk>/', likes, name='likes'),
    path('search/', search, name='search'),
    path('my_articles/', my_articles, name='my_articles'),
    path('add_article/', add_article, name='add_article'),
    path('update_article/<slug:slug>/', update_article, name='update'),



    

]
    