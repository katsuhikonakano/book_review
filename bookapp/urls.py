from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/<int:review_id>/delete', views.review_delete, name='review_delete'),

    path('books/', views.books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    path('users/<str:username>/', views.mypage, name='mypage'),
    
    path('settings/user', views.UserChangeView.as_view(), name='user_settings'),

    path('api/reviews/<int:review_id>/like/', api.LikeReview.as_view(), name='like_review_api'),
    path('api/books/<int:book_id>/mark/', api.MarkBook.as_view(), name='mark_book_api'),
    path('api/books/<int:book_id>/is_reviewed/', api.IsReviewed.as_view(), name='is_reviewed_api'),

    path('login/', auth_views.LoginView.as_view(template_name='bookapp/login.html', form_class=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
