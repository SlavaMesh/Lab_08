from django.urls import path
from .views import NewsList, PostDetail, SearchList, ADD, Delete, Update, CategoryListView, subscribe


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view()),
    path('add/', ADD.as_view(), name='post_add'),
    path('<int:pk>/delete/', Delete.as_view(), name='post_delete'),
    path('<int:pk>/edit/', Update.as_view(), name='post_update'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]

